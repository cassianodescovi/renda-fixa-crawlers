from abc import abstractmethod
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup as bs
from bs4 import FeatureNotFound

from decorators import execution_time
from loggers import logger
from utils.files import get_lattest_file, path_builder, read_configs


class AbsParser:
    """
    Abstract base class for parsing data
    """

    @abstractmethod
    def parse(self):
        pass


class SelicBacenParser(AbsParser):
    def __init__(self, configs_path: dict):
        self.configs_path = configs_path
        self.configs = read_configs(self.configs_path, "parser", "selic", "bacen")

    @execution_time
    def parse(self) -> pd.DataFrame:
        """
        Função para processar o arquivo de texto com os dados da SELIC e carregar em um DataFrame
        :return:
        """

        try:
            file_path = get_lattest_file(folder=Path(self.configs["local_read"]))

            with open(file_path, "r", encoding="utf-8") as file:
                soup = bs(file, "html.parser")

            table = soup.find("table", {"id": "historicotaxasjuros"})

            data = []
            rows = table.find("tbody").find_all("tr")

            for row in rows:
                cols = row.find_all("td")
                cols = [col.text.strip() for col in cols]

                if len(cols) == 8:
                    numero_reuniao = cols[0]
                    data_reuniao = cols[1]
                    vies = cols[2] if cols[2] else None
                    vigencia = cols[3]
                    meta_selic = cols[4]
                    tban = cols[5] if cols[5] else None
                    taxa_selic_percentual = cols[6] if cols[6] else None
                    taxa_selic_anual = cols[7] if cols[7] else None

                    data.append(
                        [
                            numero_reuniao,
                            data_reuniao,
                            vies,
                            vigencia,
                            meta_selic,
                            tban,
                            taxa_selic_percentual,
                            taxa_selic_anual,
                        ]
                    )

            df = pd.DataFrame(
                data,
                columns=[
                    "num_reuniao",
                    "data",
                    "vies",
                    "per_vigencia",
                    "meta_selic",
                    "tban",
                    "taxa_Selic",
                    "taxa_selic_aa",
                ],
            )

            df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
            df["meta_selic"] = df["meta_selic"].str.replace(",", ".").astype(float)
            df["taxa_Selic"] = df["taxa_Selic"].str.replace(",", ".").astype(float)
            df["taxa_selic_aa"] = (
                df["taxa_selic_aa"].str.replace(",", ".").astype(float)
            )
            df["tban"] = df["tban"].str.replace(",", ".").astype(float)

            path = path_builder(self.configs, transaction="local_write", local=True)

            df.to_csv(path, index=False)

            return df

        except (
            FileNotFoundError,
            IOError,
            AttributeError,
            ValueError,
            KeyError,
            TypeError,
            FeatureNotFound,
            Exception,
        ) as e:
            logger.error(f"Erro ao processar os dados da SELIC Bacen: {str(e)}")

            return pd.DataFrame()


class SelicIpeaParser(AbsParser):
    """
    Parser for IPEA data
    """

    def __init__(self, configs_path: dict):
        self.configs_path = configs_path
        self.configs = read_configs(self.configs_path, "parser", "selic", "ipea")

    @execution_time
    def parse(self) -> pd.DataFrame:
        try:
            file_path = get_lattest_file(folder=Path(self.configs["local_read"]))

            with open(file_path, "r", encoding="utf-8") as file:
                soup = bs(file, "html.parser")

            table = soup.find("table", {"id": "grd_DXMainTable"})

            data = []
            rows = table.find_all("tr")[1:]  # Skip header row
            for row in rows:
                cols = row.find_all("td")
                cols = [col.text.strip() for col in cols]
                data.append(cols)

            filtered_data = data[2:]

            df = pd.DataFrame(filtered_data, columns=["Data", "Taxa Selic Over"])

            df["Data"] = pd.to_datetime(df["Data"], format="%Y.%m")
            df["Data"] = df["Data"].dt.strftime("%m/%Y")
            df["Taxa Selic Over"] = df["Taxa Selic Over"].str.replace(".", "")
            df["Taxa Selic Over"] = (
                df["Taxa Selic Over"].str.replace(",", ".").astype(float)
            )

            return df

        except (
            FileNotFoundError,
            IOError,
            AttributeError,
            ValueError,
            KeyError,
            TypeError,
            FeatureNotFound,
            Exception,
        ) as e:
            logger.error(f"Erro ao processar os dados da SELIC Bacen: {str(e)}")

            return pd.DataFrame()  # Return an empty DataFrame on error
