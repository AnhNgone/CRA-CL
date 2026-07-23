import pandas as pd

from src.paths import ACCEPTED_RAW, REJECTED_RAW
from src.data.filter_vintage import (
    LOAN_TERM,
    VINTAGE_START,
    VINTAGE_END,
    drop_leakage_columns,
    filter_vintage,
)

# Rejected file la 27.6M dong nhung chi can vai cot cho RQ5 (approval rate
# xap xi) - doc toan bo se OOM tren may thong thuong. Loc theo cung vintage
# window luon trong luc doc theo chunk de giu memory thap.
REJECTED_USECOLS = [
    "Amount Requested",
    "Application Date",
    "Risk_Score",
    "Debt-To-Income Ratio",
    "State",
    "Employment Length",
]


def load_accepted_raw(usecols=None) -> pd.DataFrame:
    return pd.read_csv(ACCEPTED_RAW, usecols=usecols, low_memory=False)


def load_accepted_vintage(
    start: str = VINTAGE_START,
    end: str = VINTAGE_END,
    term: str = LOAN_TERM,
    chunksize: int = 200_000,
) -> pd.DataFrame:
    """Doc accepted theo chunk, loc vintage + loai leakage ngay tren tung chunk.

    Accepted goc la 2.26M dong x 151 cot (~3.3GB khi load full) nhung sau khi
    loc vintage 2015-2017 chi con ~640K dong - doc full roi moi loc gay peak
    memory khong can thiet, dac biet khi ket hop voi rejected trong cung notebook.
    """
    # id/member_id ep ve str: de nghi khi doc theo chunk, mot so chunk suy ra int64,
    # so khac suy ra object (do gia tri rong o cuoi file) -> lech dtype khi concat.
    reader = pd.read_csv(
        ACCEPTED_RAW,
        low_memory=False,
        chunksize=chunksize,
        dtype={"id": str, "member_id": str},
    )
    chunks = [
        drop_leakage_columns(filter_vintage(chunk, start=start, end=end, term=term))
        for chunk in reader
    ]
    return pd.concat(chunks, ignore_index=True)


def load_rejected_vintage(
    start: str = VINTAGE_START, end: str = VINTAGE_END, chunksize: int = 1_000_000
) -> pd.DataFrame:
    reader = pd.read_csv(
        REJECTED_RAW,
        usecols=REJECTED_USECOLS,
        parse_dates=["Application Date"],
        chunksize=chunksize,
    )
    filtered_chunks = [
        chunk.loc[chunk["Application Date"].between(start, end)] for chunk in reader
    ]
    return pd.concat(filtered_chunks, ignore_index=True)
