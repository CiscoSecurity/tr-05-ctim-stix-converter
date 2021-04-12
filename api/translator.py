from datetime import datetime, timedelta

from bundlebuilder.exceptions import ValidationError, SchemaError
from bundlebuilder.models import (
    Sighting, Bundle, ObservedTime, Observable,
    Indicator, ValidTime, Relationship
)
from bundlebuilder.session import Session
from requests.exceptions import HTTPError

from api.constants import NUMBER_OF_DAYS_INDICATOR_IS_VALID, DEFAULT_SOURCE
from api.exceptions import (
    NoObservablesFoundError,
    BundleBuilderError,
    TRError
)


def translate(args, tr_client):
    observables = extract_observables(
        args['content'], tr_client, exclude=args['exclude']
    )

    session_ = Session(
        external_id_prefix=args['external_id_prefix'],
        source=args['source'],
        source_uri=args['source_uri']
    )
    return build_bundle(observables, args['title'], session_)


def extract_observables(content, tr_client, exclude=None):
    exclude = exclude or []
    try:
        observables = tr_client.inspect.inspect({'content': content})
        observables = [
            ob for ob in observables if ob['value'] not in exclude
        ]

    except HTTPError as error:
        raise TRError(error)

    if not observables:
        raise NoObservablesFoundError()

    return observables


def build_bundle(observables, title, session_):
    def format_time(time):
        return f'{time.isoformat(timespec="seconds")}Z'

    try:
        with session_.set():
            now = datetime.now()
            now_str = format_time(now)

            bundle = Bundle()

            sighting = Sighting(
                confidence='High',
                count=1,
                observed_time=ObservedTime(
                    start_time=now_str,
                    end_time=now_str,
                ),
                observables=[
                    Observable(**ob) for ob in observables
                ],
                title=title,
                internal=False
            )

            bundle.add_sighting(sighting)

            indicator = Indicator(
                producer=DEFAULT_SOURCE,
                valid_time=ValidTime(
                    start_time=now_str,
                    end_time=format_time(
                        now + timedelta(NUMBER_OF_DAYS_INDICATOR_IS_VALID)
                    ),
                ),
                confidence='High',
                title=title,
            )

            bundle.add_indicator(indicator)

            relationship_from_sighting_to_indicator = Relationship(
                relationship_type='member-of',
                source_ref=sighting,
                target_ref=indicator,
                short_description=f'{sighting} is member-of {indicator}',
            )

            bundle.add_relationship(relationship_from_sighting_to_indicator)

            return bundle

    except (ValidationError, SchemaError) as error:
        raise BundleBuilderError(error)
