class Charts:
    def __init__(self, chart_data, total_earnings, total_orders):
        self.__chart_data = chart_data
        self.__total_earnings = total_earnings
        self.__total_orders = total_orders

    def get_chart_data(self):
        return self.__chart_data
    
    def get_total_earnings(self):
        return self.__total_earnings
    
    def get_total_orders(self):
        return self.__total_orders
    
    def set_chart_data(self, chart_data):
        self.__chart_data = chart_data    

    def set_total_earnings(self, total_earnings):
        self.__total_earnings = total_earnings

    def set_total_orders(self, total_orders):
        self.__total_orders = total_orders