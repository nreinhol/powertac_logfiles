import matplotlib.pyplot as plt
from powertac_logfiles import data
from powertac_logfiles import visualize
import os
import pandas as pd
import seaborn as sns


def visualize_broker_accounting():
    for file_name in os.listdir(data.PROCESSED_DATA_PATH):
        if not file_name.find('BrokerAccounting') == -1:
            df_broker_accounting = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal=',')
            rename_columns = {'ts': 'timeslot',
                              'dow': 'day_of_week',
                              'hod': 'hour_of_day',
                              'broker': 'broker',
                              'ttx-sc': 'Tariff_transaction_status_update_credit',
                              'ttx-sd': 'Tariff_transaction_status_update_debit',
                              'ttx-uc': 'Tariff_transaction_(prod./cons.)_of_customers_credit',
                              'ttx-ud': 'Tariff_transaction_(prod./cons.)_of_customers_debit',
                              'mtx-c': 'Wholesale_market_transaction_credit',
                              'mtx-d': 'Wholesale_market_transaction_debit',
                              'btx-c': 'Balancing_transaction_credit',
                              'btx-d': 'Balancing_transaction_debit',
                              'dtx-c': 'Distribution_transaction_(kWh/transp.)_credit',
                              'dtx-d': 'Distribution_transaction_(kWh/transp.)_debit',
                              'ctx-c': 'Capacity_transaction credit',
                              'ctx-d': 'Capacity_transaction debit',
                              'bce-c': 'Balancing_control_event_credit',
                              'bce-d': 'Balancing_control_event_debit',
                              'bank-c': 'Banking_transaction_credit',
                              'bank-d': 'Banking_transaction_debit',
                              'cash': 'Net_cash_position'}
            df_broker_accounting.rename(columns=rename_columns, inplace=True)
            df_broker_accounting_transformed = df_broker_accounting.melt(
                id_vars=['timeslot', 'day_of_week', 'hour_of_day', 'broker', 'Net_cash_position'], var_name='performance_driver', value_name='value')
            df_broker_accounting_transformed_grouped = df_broker_accounting_transformed.drop(['timeslot', 'day_of_week', 'hour_of_day', 'Net_cash_position'], axis=1).groupby(['broker', 'performance_driver'], as_index=False).sum()

            # net cash position needs to be excluded! only the last value should be plottet!
            last_timeslot = max(df_broker_accounting['timeslot'].unique())
            for broker in df_broker_accounting['broker'].unique():
                final_cash_position_of_broker = df_broker_accounting[df_broker_accounting['broker']==broker]
                final_cash_position_of_broker = final_cash_position_of_broker[final_cash_position_of_broker['timeslot']==last_timeslot]
                final_cash_position_of_broker = final_cash_position_of_broker['Net_cash_position'].iloc[0]
                df_broker_accounting_transformed_grouped = df_broker_accounting_transformed_grouped.append({'broker': broker, 'performance_driver': 'Final_net_cash_position', 'value': final_cash_position_of_broker}, ignore_index=True)

            fig = plt.figure(figsize=(15, 10))
            ax1 = fig.add_subplot(111)
            g = sns.swarmplot(ax=ax1,
                                x='performance_driver',
                                y='value',
                                hue='broker',
                                size=10,
                                data=df_broker_accounting_transformed_grouped)
            g.set_xticklabels(g.get_xticklabels(), rotation=90)
            fig.tight_layout()
            plt.savefig('{}/{}_broker_accounting'.format(data.OUTPUT_DIR, visualize.grep_game_name(file_name)), bbox_inches="tight")
            print("Successfully created broker accounting performance driver plot.")


if __name__ == '__main__':
    visualize_broker_accounting()
