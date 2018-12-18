import pymysql
import pandas as pd


def __connect_to_local_database():
    conn = pymysql.connect(host='localhost', user='root', passwd='Sorge6,aastet', db='ewiis3')
    return conn


def execute_sql_query(sql_query):
    conn = __connect_to_local_database()
    df_mysql = pd.read_sql(sql_query, con=conn)
    conn.close()
    return df_mysql


def load_tariff_transactions():
    sql_statement = "SELECT * FROM `tariff_transaktion`"
    df_tariff_transactions = execute_sql_query(sql_statement)
    return df_tariff_transactions


def load_balance_report():
    sql_statement = "SELECT t.* FROM ewiis3.balance_report t"
    df_balance_report = execute_sql_query(sql_statement)
    return df_balance_report


def load_weather_report():
    sql_statement = "SELECT t.* FROM ewiis3.weather_report t"
    df_weather_report = execute_sql_query(sql_statement)
    return df_weather_report


def load_balancing_transactions():
    sql_statement = "SELECT t.* FROM ewiis3.balancing_transaction t"
    df_balancing_transactions = execute_sql_query(sql_statement)
    return df_balancing_transactions


def load_capacity_transactions():
    sql_statement = "SELECT t.* FROM ewiis3.capacity_transaction t"
    df_capacity_transactions = execute_sql_query(sql_statement)
    return df_capacity_transactions


def load_distribution_reports():
    sql_statement = "SELECT t.* FROM ewiis3.distribution_report t"
    df_distribution_reports = execute_sql_query(sql_statement)
    return df_distribution_reports


def load_orderbooks():
    sql_statement = "SELECT t.* FROM ewiis3.orderbook_order t"
    df_orderbook = execute_sql_query(sql_statement)
    return df_orderbook


def load_cleared_trades():
    sql_statement = "SELECT t.* FROM ewiis3.cleared_trade t"
    df_cleared_trades = execute_sql_query(sql_statement)
    return df_cleared_trades


def load_tariff_specifications():
    sql_statement = "SELECT t.* FROM ewiis3.tariff_specification t"
    df_tariff_specification = execute_sql_query(sql_statement)
    return df_tariff_specification


def load_rates():
    sql_statement = "SELECT r.*, ts.brokerName, ts.gameId, ts.powerType FROM ewiis3.rate  r LEFT JOIN ewiis3.tariff_specification ts ON r.tariffSpecificationId = ts.tariffSpecificationId"
    df_rates = execute_sql_query(sql_statement)
    return df_rates
