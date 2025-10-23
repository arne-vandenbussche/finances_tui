#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 10:14:13 2025

@author: arnevandenbussche
"""

import sqlite3
from pathlib import Path
import logging
from model.transactie import Transactie
from datetime import date, datetime
from environs import Env # https://pypi.org/project/environs/

env = Env()
env.read_env() # read .env file if it exists
DATABASE_NAME = env.str("DATABASE")

def is_valid_date(date_string: str) -> bool:
    try:
        datetime.strptime(date_string, '%Y-%m-%d').date()
        return True
    except (TypeError, ValueError):
        return False


def convert_transaction_row_to_object(transaction_row: tuple) -> Transactie:
    tr_id = transaction_row[0]
    if is_valid_date(transaction_row[1]):
        tr_datum = datetime.strptime(transaction_row[1], "%Y-%m-%d").date()
    else:
        tr_datum = date(1000,1,1)
        logger = logging.getLogger(__name__)
        logger.warning(f"Transaction with id={tr_id} has an invalid date")
    tr_bedrag = transaction_row[2]
    tr_betaalwijze = transaction_row[3]
    tr_rekeningnummer = transaction_row[4]
    tr_van_aan = transaction_row[5]
    tr_beschrijving = transaction_row[6]
    tr_factuurnummer = transaction_row[7]
    if transaction_row[8] == None or transaction_row[8] == "":
        tr_factuurdatum = date(1,1,1)
    elif is_valid_date(transaction_row[8]):
        tr_factuurdatum = datetime.strptime(transaction_row[8], "%Y-%m-%d").date()
    else:
        tr_factuurdatum = date(1,1,1)
        logger = logging.getLogger(__name__)
        logger.warning(f"Transaction with id={tr_id} has an invalid date for factuurdatum")
    tr_categorie = transaction_row[9]
    tr_actuele_rekeningstand = transaction_row[10]
    return Transactie(id=tr_id, datum=tr_datum, bedrag=tr_bedrag, betaalwijze=tr_betaalwijze,
                      rekeningnummer= tr_rekeningnummer, van_aan=tr_van_aan,
                      beschrijving=tr_beschrijving, factuurnummer=tr_factuurnummer,
                      factuurdatum=tr_factuurdatum, categorie=tr_categorie,
                      actuele_rekeningstand=tr_actuele_rekeningstand)


def get_connection() -> sqlite3.Connection:
    logger = logging.getLogger(__name__)
    db_file_name = DATABASE_NAME
    db_directory = Path.cwd()
    full_db_path = db_directory / db_file_name
    is_new_db = not full_db_path.exists()

    # Connect to database. The database will be created if it does not exists
    conn = sqlite3.connect(full_db_path)
    logger.info(f"Connecting to database on {full_db_path}")
    # If the database is not there, I will intialize it, crdating the tables
    if is_new_db:
        logger.info(f"Database on {full_db_path} missing. Creating database.")
        initialize_database(conn)

    return conn


def initialize_database(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE transacties (
        id integer primary key,
        datum date not null,
        bedrag double not null default 0,
        betaalwijze text not null,
        rekeningnummer text,
        van_aan text,
        beschrijving text,
        factuurnummer text,
        factuurdatum date,
        categorie text,
        actuele_rekeningstand double);
    """)
    conn.commit()

def get_all_transactions() -> list[Transactie]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacties order by datum desc")
    all_row_transactions = cursor.fetchall()
    conn.close()
    transaction_list = []
    for transaction in all_row_transactions:
        transaction_list.append(convert_transaction_row_to_object(transaction))
    return transaction_list


def get_transaction_by_id(transaction_id: int) -> Transactie:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacties WHERE id = ?", (transaction_id,))
    transaction_row = cursor.fetchone()
    conn.close()
    if transaction_row:
        return convert_transaction_row_to_object(transaction_row)
    else:
        return None


def get_transactions_by_date(transaction_date: date) -> list[Transactie]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacties WHERE datum = ?", (transaction_date,))
    rows = cursor.fetchall()
    conn.close()
    transaction_list = [convert_transaction_row_to_object(row) for row in rows]
    return transaction_list

def get_transaction_by_description(part_description: str) -> list[Transactie]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacties WHERE LOWER(beschrijving) LIKE '%' || LOWER(?) || '%' OR LOWER(van_aan) LIKE '%' || LOWER(?) || '%'", (part_description, part_description))
    rows = cursor.fetchall()
    conn.close()
    transaction_list = [convert_transaction_row_to_object(row) for row in rows]
    return transaction_list

def save_transaction(transaction: Transactie) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    if transaction.id == 0:
        # Create a new transaction
        cursor.execute("""
            INSERT INTO transacties
            (datum, bedrag, betaalwijze, rekeningnummer, van_aan, beschrijving,
            factuurnummer, factuurdatum, categorie, actuele_rekeningstand)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (transaction.datum, transaction.bedrag, transaction.betaalwijze,
                  transaction.rekeningnummer, transaction.van_aan, transaction.beschrijving,
                  transaction.factuurnummer, transaction.factuurdatum, transaction.categorie,
                  transaction.actuele_rekeningstand))
    else:
        # Update an existing transaction
        cursor.execute("""
            UPDATE transacties
            SET datum=?, bedrag=?, betaalwijze=?, rekeningnummer=?, van_aan=?, beschrijving=?,
            factuurnummer=?, factuurdatum=?, categorie=?, actuele_rekeningstand=?
            WHERE id=?
            """, (transaction.datum, transaction.bedrag, transaction.betaalwijze,
                  transaction.rekeningnummer, transaction.van_aan, transaction.beschrijving,
                  transaction.factuurnummer, transaction.factuurdatum, transaction.categorie,
                  transaction.actuele_rekeningstand, transaction.id))
    conn.commit()
    conn.close()
