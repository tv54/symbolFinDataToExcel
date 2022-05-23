from openpyxl.chart.reference import Reference
from openpyxl.chart.line_chart import LineChart
from openpyxl.chart.bar_chart import BarChart
from openpyxl.chart.axis import DateAxis
import src.package.subpackage.othersrc.Constants as Constants
from src.package.subpackage.handlers.StyleHandler import StyleHandler

class ChartingHandler():

    def __setBenchmarkChart(self, ws, tempChart, benchmarkCol, row1, series, chartType="line", row2=0, toCol="", horizontalData=False, secondAxis=False, secondAxisYTitle="", secondAxisCatColumn=0):
        if(not horizontalData):
            tempChart.add_data(Reference(ws, min_col=Constants.COLUMN_NAMES.index(benchmarkCol)+1, min_row=row1, max_row=row2), titles_from_data=True)
        else:
            tempChart.add_data(Reference(ws, min_col=Constants.COLUMN_NAMES.index(benchmarkCol)+1, max_col=Constants.COLUMN_NAMES.index(toCol)+1, min_row=row1), titles_from_data=True, from_rows=horizontalData)

        if(secondAxis):
            # ---- x axis ----
            tempChart.x_axis=DateAxis(crossAx=100)
            # ---- y axis ----
            tempChart.y_axis.title=secondAxisYTitle
            tempChart.y_axis.axId=200
            tempChart.y_axis.crosses="max"
            tempChart.y_axis.majorGridlines=None
            tempChart.y_axis.crossAx=500
            tempChart.legend.position=Constants.CHART_LEGEND_POSITION
            tempChart.set_categories(Reference(ws, min_col=Constants.COLUMN_NAMES.index(secondAxisCatColumn)+1, min_row=row1+1, max_row=row2))

        if(chartType=="line"):
            tempChart.series[series].spPr.line.solidFill=Constants.DARK_BROWN_COLOR
            tempChart.series[series].spPr.line.dashStyle="sysDash"
            return

        tempChart.series[series].spPr.solidFill=Constants.DARK_BROWN_COLOR

    def chart(
                self, 
                ws, 
                chartType="line", 
                column1="A", 
                column2="B", 
                row1=1, 
                row2=2, 
                title="", 
                xAxisTitle="", 
                yAxisTitle="", 
                titlesFromData=True, 
                chartCoords="", 
                benchmarkCol="", 
                horizontalData=False, 
                secondAxis=False, 
                SecondAxisYTitle="", 
                extraElemReferences=None,
                lineMarkers=False, 
                stacked=False, 
                yearOnly=False,
                secondWs=None,
                secondWsChartCoords="A1"
                ):
        """Add chart to worksheet

        Args:
            chartType (str, optional): 'line' or 'bar'. Defaults to "line".
            column1 (str, optional): Column of first point of data. Defaults to "A".
            column2 (str, optional): Column of last point of data (none if data selection is vertical). Defaults to "B".
            row1 (int, optional): Row number of first point of data. Defaults to 1.
            row2 (int, optional): Row number of last point of data (none if data selection is vertical). Defaults to 2.
            title (str, optional): Chart title. Defaults to "".
            titlesFromData (bool, optional): Get axis titles from data. Defaults to True.
            chartCoords (str, optional): '<column><row>'. Defaults to "".
            benchmarkCol (str, optional): Benchmark data as second function. Defaults to "".
            secondAxis (bool, optional): Secondary Y axis. Defaults to False.
            extraElemReferences (Reference, optional): Array of references for extra data. Defaults to None.
            yearOnly (bool, optional): Display date as 'yyyy'. Defaults to False.
            secondWs (Worksheet, optional): Second worksheet to add the chart to. Defaults to None.
            secondWsChartCoords (str, optional): '<column><row>'. Defaults to "A1".
        """

        match chartType:
            case "line":
                chart=LineChart()
            case "bar":
                chart=BarChart()

        if(not horizontalData):
            chart.add_data(Reference(ws, min_col=Constants.COLUMN_NAMES.index(column2)+1, min_row=row1, max_row=row2), titles_from_data=titlesFromData)
            chart.set_categories(Reference(ws, min_col=Constants.COLUMN_NAMES.index(column1)+1, min_row=row1+1, max_row=row2))
        else:
            chart.add_data(Reference(ws, min_col=Constants.COLUMN_NAMES.index(column1)+1, max_col=Constants.COLUMN_NAMES.index(column2)+1, min_row=row1), titles_from_data=titlesFromData, from_rows=horizontalData)
            chart.set_categories(Reference(ws, min_col=Constants.COLUMN_NAMES.index(column1)+2, max_col=Constants.COLUMN_NAMES.index(column2)+1, min_row=row2))
            yearOnly=True

        StyleHandler.defaultChartStyle(chart, title, yAxisTitle, xAxisTitle, stacked, chartType=chartType, yearOnly=yearOnly, lineMarkers=lineMarkers, series=0)

        if(benchmarkCol):
            # ---- Benchmark on primary axis ----
            if(not secondAxis):
                series=1
                self.__setBenchmarkChart(ws, chart, benchmarkCol, row1, series, row2=row2, horizontalData=horizontalData)
            # ---- Benchmark second axis ----
            else:
                match chartType:
                    case "line":
                        chart2=LineChart()
                    case "bar":
                        chart2=BarChart()
                series=0
                self.__setBenchmarkChart(ws, chart2, benchmarkCol, row1, series, chartType=chartType, row2=row2, secondAxis=secondAxis, secondAxisYTitle=SecondAxisYTitle, secondAxisCatColumn=column1)
                chart += chart2

        if(extraElemReferences):
            for ref in extraElemReferences:
                chart.add_data(ref, titles_from_data=titlesFromData, from_rows=horizontalData)
            if(benchmarkCol):
                series=2
            else:
                series=1

            match chartType:
                case "line":
                    chart.series[series].spPr.line.solidFill=Constants.DARK_GRAY_COLOR
                case "bar":
                    chart.series[series].spPr.solidFill=Constants.DARK_GRAY_COLOR
                
        chartCoords and ws.add_chart(chart, chartCoords)
        secondWs and secondWs.add_chart(chart, secondWsChartCoords)