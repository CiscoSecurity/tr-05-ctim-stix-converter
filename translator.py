import json
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime, timedelta

from bundlebuilder.models import (
    Sighting, Bundle, ObservedTime, Observable,
    Indicator, ValidTime, Relationship
)
from bundlebuilder.session import Session
from threatresponse import ThreatResponse

DEFAULT_REGION = 'us'
DEFAULT_SOURCE = 'CTIM-STIX Translator'
DEFAULT_SOURCE_URI = (
    'https://github.com/CiscoSecurity/tr-05-ctim-stix-translator'
)
DEFAULT_EXTERNAL_ID_PREFIX = 'ctim-stix-translator'
NUMBER_OF_DAYS_INDICATOR_IS_VALID = 30


class NoObservablesFound(Exception):
    pass


def extract_observables(file_name, tr_client, exclude=None):
    exclude = exclude or []
    with open(file_name) as file:
        observables = tr_client.inspect.inspect({'content': file.read()})
        observables = [ob for ob in observables if ob['value'] not in exclude]
        return observables


def build_bundle(observables, file_name, session_):
    def format_time(time):
        return f'{time.isoformat(timespec="seconds")}Z'

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


def get_arguments():
    parser = ArgumentParser(
        description='Transforms STIX data into CTIM Bundle.',
        epilog=('Required environment variables: CTR_CLIENT, CTR_PASSWORD. \n'
                'Optional environment variables: CTR_REGION (default: us).'),
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('file', help='STIX file to process')
    parser.add_argument(
        '-s', '--source', help='Source Name',
        type=str, default=DEFAULT_SOURCE, metavar='',
    )
    parser.add_argument(
        '-u', '--source_uri', help='Source Uri',
        type=str, default=DEFAULT_SOURCE_URI, metavar='',
    )
    parser.add_argument(
        '-p', '--external_id_prefix', help='External ID Prefix',
        type=str, default=DEFAULT_EXTERNAL_ID_PREFIX, metavar='',
    )
    parser.add_argument(
        '-e', '--exclude', help='Observables to exclude',
        type=str, action='append', metavar='',
    )
    return parser.parse_args()


def main():
    try:
        args = get_arguments()
        tr_client = ThreatResponse(
            client_id=os.environ['CTR_CLIENT'],
            client_password=os.environ['CTR_PASSWORD'],
            region=os.getenv('CTR_REGION', DEFAULT_REGION)
        )

        file_name = os.path.basename(args.file)
        observables = extract_observables(
            file_name, tr_client, exclude=args.exclude
        )
        if not observables:
            raise NoObservablesFound(f'No observables found in {file_name}')

        session_ = Session(
            external_id_prefix=args.external_id_prefix,
            source=args.source,
            source_uri=args.source_uri
        )
        bundle = build_bundle(observables, file_name, session_)
        print(json.dumps(bundle.json, indent=4, sort_keys=True))

    except Exception as e:
        print('Error occurred: ', str(e))


if __name__ == '__main__':
    main()
