bgcolor = "'" + "#f0f0f0" + "'"

def getHTMLFromDataBarChart(endlist1, endlist2):

    total1 = endlist1[1] + endlist1[2] + endlist1[3]
    total2 = endlist2[1] + endlist2[2] + endlist2[3]

    width = "530px"
    height = "500px" 
 

    endlist1[0] ="(" + str(int(total1)) + " total) " + endlist1[0].replace("-", " ")
    endlist2[0] ="(" + str(int(total2)) + " total) " + endlist2[0].replace("-", " ")

    listOfStuff = []
    listOfStuff.append(['Device', 'Positive', 'Negative', 'Neutral'])
    listOfStuff.append(endlist1)
    listOfStuff.append(endlist2)

    
    fulltitle =  ""  

    html = '''<script type="text/javascript" src="https://www.google.com/jsapi"></script> <script type="text/javascript">  google.load("visualization", "1", {packages:["corechart"]});  google.setOnLoadCallback(drawChart);  function drawChart() { var data = google.visualization.arrayToDataTable(''' + str(listOfStuff) + '''); var options = {width: 530, height: 500,backgroundColor: ''' + bgcolor + ''',   title: ' ''' + fulltitle + ''' ',  hAxis: {title: '', titleTextStyle: {color: 'red'}} }; var chart = new google.visualization.ColumnChart(document.getElementById('chart_div')); chart.draw(data, options);  } </script> <div id="chart_div" style="width: ''' + width + '''; height: ''' + height + ''';"></div> '''

    return html

def getHTMLFromDataDonut(list1, list2): 

    title1 = list1.pop(0) 
    title2 = list2.pop(0)
    
    endlist1 = []
    endlist2 = []
    
    endlist1.append(["Positive", list1[0]])
    endlist1.append(["Negative", list1[1]])
    endlist1.append(["Neutral", list1[2]]) 

    endlist2.append(["Positive", list2[0]])
    endlist2.append(["Negative", list2[1]])
    endlist2.append(["Neutral", list2[2]]) 

    total1 = list1[0] + list1[1] + list1[2]
    total2 = list2[0] + list2[1] + list2[2]
   
    width = "400px"
    height = "480px"
     
    endlist1.insert(0,['Fraction', 'Positivity'])
    titleTxt1 = "'(" + str(int(total1)) + " total) " + title1.replace("-", " ") + "'"
    titleId1 = title1 + "'"
 
     
    endlist2.insert(0,['Fraction', 'Positivity'])
    titleTxt2 = "'(" + str(int(total2)) + " total) " + title2.replace("-", " ") + "'" 
    titleId2 = title2 + "'"

    html = '''<script type="text/javascript" src="https://www.google.com/jsapi"></script> <script type="text/javascript">  google.load("visualization", "1", {packages:["corechart"]});  google.setOnLoadCallback(drawChart);  function drawChart() { var data = google.visualization.arrayToDataTable(''' + str(endlist1) + ''' ); var options = { backgroundColor: ''' + bgcolor + ''',   title: ''' + titleTxt1 + ''',   pieHole: 0.4, }; var chart = new google.visualization.PieChart(document.getElementById('donutchart''' + titleId1 + ''')); chart.draw(data, options);  }    </script> ''' + '''<script type="text/javascript" src="https://www.google.com/jsapi"></script> <script type="text/javascript">  google.load("visualization", "1", {packages:["corechart"]});  google.setOnLoadCallback(drawChart);  function drawChart() { var data = google.visualization.arrayToDataTable(''' + str(endlist2) + ''' ); var options = {backgroundColor: ''' + bgcolor + ''',    title: ''' + titleTxt2 + ''',   pieHole: 0.4, }; var chart = new google.visualization.PieChart(document.getElementById('donutchart''' + titleId2 + ''')); chart.draw(data, options);  }    </script> '''  + '''<div><div id="donutchart'''+title1+'''"  style="display: inline-block;height:''' + height + '''; width:''' + width + ''';"> </div><div id="donutchart'''+title2+'''"  style="display: inline-block;height:''' + height + '''; width:''' + width + ''';"> </div></div>'''
    return html




s1 = ["Apple Ipad version xy", 111,222,333]
s2 = ["Nexus 7 version xy", 151,222,333]
 
f = open('chart2.html','w') 