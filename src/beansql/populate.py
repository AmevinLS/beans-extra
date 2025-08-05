from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from beancount.loader import load_file
from beancount.core.data import Transaction

from beansql.schemas import (
    Base,
    PostingDB,
    TransactionDB,
    TransactionLinkDB,
    TransactionTagDB,
)


def transaction_to_db(trans: Transaction) -> TransactionDB:
    postings = [
        PostingDB(
            account=post.account,
            units_number=float(post.units.number) if post.units else None,
            units_currency=post.units.currency if post.units else None,
            cost_number=float(post.cost.number) if post.cost else None,
            cost_currency=post.cost.currency if post.cost else None,
            price_number=float(post.price.number) if post.price else None,
            price_currency=post.price.currency if post.price else None,
            flag=post.flag,
        )
        for post in trans.postings
    ]

    tags = [TransactionTagDB(tag_name=tag_name) for tag_name in trans.tags]
    links = [TransactionLinkDB(link_name=link_name) for link_name in trans.links]

    return TransactionDB(
        trans_date=trans.date,
        flag=trans.flag,
        payee=trans.payee,
        narration=trans.narration,
        tags=tags,
        links=links,
        postings=postings,
    )


def main():
    db_transactions: list[TransactionDB] = []

    entries, errors, other = load_file(R"D:\Repos\finances\main.bean")
    for entry in entries:
        if isinstance(entry, Transaction):
            db_transactions.append(transaction_to_db(entry))

    engine = create_engine(R"sqlite:///D:\Repos\beansql\my.db")

    with Session(engine) as session:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        session.add_all(db_transactions)
        session.commit()


if __name__ == "__main__":
    main()
