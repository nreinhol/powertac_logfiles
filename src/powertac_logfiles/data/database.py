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


def load_customer_prosumption():
    sql_statement = 'SELECT postedTimeslotIndex, SUM(kWH) FROM ewiis3.tariff_transaktion WHERE (txType = "CONSUME" OR txType = "PRODUCE") GROUP BY postedTimeslotIndex'
    df_customer_prosumption = execute_sql_query(sql_statement)
    return df_customer_prosumption


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


def load_order_submits():
    sql_statement = "SELECT t.* FROM ewiis3.order_submit t"
    df_order_submits = execute_sql_query(sql_statement)
    return df_order_submits


def load_tariff_evaluation_metrics():
    sql_statement = "select powerType, txType, SUM(charge), AVG(currentSubscribedPopulation) from ewiis3.tariff_transaktion group by powerType, txType;"
    df_tariff_evaluation = execute_sql_query(sql_statement)
    return df_tariff_evaluation


def load_rates():
    sql_statement = "SELECT r.*, ts.brokerName, ts.gameId, ts.powerType FROM ewiis3.rate  r LEFT JOIN ewiis3.tariff_specification ts ON r.tariffSpecificationId = ts.tariffSpecificationId"
    df_rates = execute_sql_query(sql_statement)
    return df_rates


def load_grid_imbalance_prediction():
    try:
        sql_statement = "SELECT t.* FROM ewiis3.imbalance_prediction t"
        df_imbalance = execute_sql_query(sql_statement)
    except Exception as E:
        df_imbalance = pd.DataFrame()
    return df_imbalance


def load_all_game_ids():
    try:
        sql_statement = "SELECT DISTINCT(t.gameId) FROM ewiis3.timeslot t"
        df_imbalance = execute_sql_query(sql_statement)
        game_ids = list(df_imbalance['gameId'])
    except Exception as E:
        game_ids = []
    return game_ids


def load_customer_prosumption_prediction():
    try:
        sql_statement = "SELECT t.* FROM ewiis3.customer_prosumption_prediction t"
        df_customer_prosumption = execute_sql_query(sql_statement)
    except Exception as E:
        df_customer_prosumption = pd.DataFrame()
    return df_customer_prosumption


def load_prosumption_prediction():
    # sql_statement = 'SELECT pp.*, dr.totalConsumption, dr.totalProduction FROM (SELECT * FROM ewiis3.distribution_report WHERE distribution_report.gameId="EWIIS3_SPOT_AgentUDE17_TacTex15_cwiBroker_maxon16_1") AS dr RIGHT JOIN (SELECT * FROM ewiis3.prosumption_prediction WHERE prosumption_prediction.game_id="EWIIS3_SPOT_AgentUDE17_TacTex15_cwiBroker_maxon16_1") AS pp ON dr.timeslot = pp.target_timeslot;'
    try:
        sql_statement = "SELECT t.* FROM ewiis3.prosumption_prediction t"
        df_prosumption_prediction = execute_sql_query(sql_statement)
    except Exception as E:
        df_prosumption_prediction = pd.DataFrame()
    return df_prosumption_prediction
