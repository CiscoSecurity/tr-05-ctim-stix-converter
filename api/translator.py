import os
from datetime import datetime, timedelta

from bundlebuilder.exceptions import ValidationError, SchemaError
from bundlebuilder.models import (
    Sighting, Bundle, ObservedTime, Observable,
    Indicator, ValidTime, Relationship
)
from bundlebuilder.session import Session
from requests.exceptions import (
    ConnectionError,
    Timeout as TimeoutError,
    HTTPError
)

from api.constants import NUMBER_OF_DAYS_INDICATOR_IS_VALID, DEFAULT_SOURCE
from api.exceptions import (
    NoObservablesFoundError,
    FailedToReadFileError,
    BundleBuilderError,
    TRError
)


def translate(args, tr_client):
    file_name = os.path.basename(args['file'])
    observables = extract_observables(
        file_name, tr_client, exclude=args['exclude']
    )

    session_ = Session(
        external_id_prefix=args['external_id_prefix'],
        source=args['source'],
        source_uri=args['source_uri']
    )
    return build_bundle(observables, file_name, session_)


def extract_observables(file_name, tr_client, exclude=None):
    exclude = exclude or []
    try:
        with open(file_name) as file:
            observables = tr_client.inspect.inspect({'content': file.read()})
            observables = [
                ob for ob in observables if ob['value'] not in exclude
            ]

    except (TimeoutError, ConnectionError, HTTPError) as error:
        raise TRError(error)

    except OSError as error:
        raise FailedToReadFileError(error)

    if not observables:
        raise NoObservablesFoundError(file_name)

    return observables


def build_bundle(observables, file_name, session_):
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
                title=f'Found in {file_name}',
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
                title=f'Found in {file_name}',
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
