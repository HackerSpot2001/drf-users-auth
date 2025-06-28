from django.core.management.base import BaseCommand
from os.path import join as joinPath, dirname
from json import load as loadJson
from re import sub as substitute
from DRF_Users.models import CityMaster, CountryMaster, StateMaster


class Command(BaseCommand):
    help = "Migrate all geodata into database"

    def handle(self, *args, **options):
        self.json_path = joinPath( dirname( __file__ ) , "../../public/geodata.json"  )
        # CityMaster.objects.filter().delete()
        # StateMaster.objects.filter().delete()
        # CountryMaster.objects.filter().delete()
        with open( self.json_path, "r", encoding="utf-8" ) as f:
            cnt = 1
            jsonData = loadJson(f)
            len_json_data = len(jsonData)
            for country_obj in jsonData:
                country_name = country_obj["name"]
                country_id = self.generate_id(country_name)
                if CountryMaster.objects.filter(country_id=country_id).exists():
                    continue

                CountryMaster(
                    country_id=country_id,
                    country_name=country_name,
                    country_shortcode=country_obj["iso2"],
                    country_numeric_code=country_obj["numeric_code"],
                    country_phonecode=country_obj["phonecode"],
                    country_currency=country_obj["currency"],
                    country_currencyname=country_obj["currency_name"],
                    country_latitude=country_obj["latitude"],
                    country_longitude=country_obj["longitude"],
                ).save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"[{cnt}/{len_json_data}] Adding Country, State, and City for country: '{country_name}' ."
                    )
                )

                for state_obj in country_obj.get("states", []):
                    state_name = state_obj["name"]
                    state_id = f"{country_id}_{self.generate_id(state_name)}"
                    if StateMaster.objects.filter(state_id=state_id).exists():
                        continue

                    StateMaster(
                        state_id=state_id,
                        state_name=state_name,
                        state_shortcode=state_obj["state_code"],
                        state_latitude=state_obj["latitude"],
                        state_longitude=state_obj["longitude"],
                        country_id=country_id,
                    ).save()
                    for city in state_obj["cities"]:
                        city_name = city["name"]
                        city_id = f"{state_id}_{self.generate_id(city_name)}"
                        if CityMaster.objects.filter(city_id=city_id).exists():
                            continue

                        CityMaster(
                            city_id=f"{state_id}_{city_id}",
                            city_name=city_name,
                            city_latitude=city["latitude"],
                            city_longitude=city["longitude"],
                            state_id=state_id,
                        ).save()

                self.stdout.write(self.style.SUCCESS("=" * 100))
                cnt += 1

    def generate_id(self, string: str):
        string = string.upper()
        string = substitute(r"\s+", "_", string)
        return string