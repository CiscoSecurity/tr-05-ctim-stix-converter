from datetime import datetime

from bundlebuilder.exceptions import ValidationError, SchemaError
from bundlebuilder.models import (
    Sighting, Bundle, ObservedTime, Observable,
    Indicator, ValidTime, Relationship
)
from bundlebuilder.session import Session

from api.constants import INDICATOR_VALIDITY_INTERVAL
from api.exceptions import (
    NoObservablesFoundError,
    BundleBuilderError
)


def translate(args, tr_client):
    observables = extract_observables(
        args.pop('content'), tr_client, exclude=args.pop('exclude')
    )

    session_ = Session(
        external_id_prefix=args['external_id_prefix'],
        source=args['source'],
        source_uri=args['source_uri']
    )
    return build_bundle(observables, session_, args)


def extract_observables(content, tr_client, exclude=None):
    exclude = exclude or []

    observables = tr_client.inspect.inspect({'content': content})
    observables = [
        ob for ob in observables if ob['value'] not in exclude
    ]

    if not observables:
        raise NoObservablesFoundError()

    return observables


def build_bundle(observables, session_, args=None):
    def format_time(time):
        return f'{time.isoformat(timespec="seconds")}Z'

    args = {} if args is None else args
    try:
        with session_.set():
            now = datetime.now()
            now_str = format_time(now)

            bundle = Bundle()

            sighting = Sighting(
                **args.get(Sighting.type, {}),
                observed_time=ObservedTime(
                    start_time=now_str,
                    end_time=now_str,
                ),
                observables=[
                    Observable(**ob) for ob in observables
                ]
            )
            bundle.add_sighting(sighting)

            indicator = Indicator(
                **args.get(Indicator.type, {}),
                valid_time=ValidTime(
                    start_time=now_str,
                    end_time=format_time(
                        now + INDICATOR_VALIDITY_INTERVAL
                    ),
                )
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
