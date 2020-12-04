from random import randint
from time import strftime
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import pandas as pd
import neo
import mongodb

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    surname = TextField('Surname:', validators=[validators.required()])

labels = ['Tagged', 'Non Tagged']

''', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
'''

data = {'Name': [],#['Jai', 'Princi', 'Gaurav', 'Anuj'],
        'Age': [],#[27, 24, 22, 32],
        'Address': [],#['Delhi', 'Kanpur', 'Allahabad', 'Kannauj'],
        'Qualification': []}#['Msc', 'MA', 'MCA', 'Phd']}

# values = [
#     967.67, 1190.89, 1079.75, 1349.19,
#     2328.91, 2504.28, 2873.83, 4764.87,
#     4349.29, 6458.30, 9907, 16297
# ]

colors = ["#F7464A", "#46BFBD"]
''', "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"'''
def get_time():
    time = strftime("%Y-%m-%dT%H:%M")
    return time

def write_to_disk(name, surname, email):
    data = open('file.log', 'a')
    timestamp = get_time()
    data.write('DateStamp={}, Name={}, Surname={}, Email={} \n'.format(timestamp, name, surname, email))
    data.close()


def get_data():
    data = {'Node Entry Name': [],
            'Node Protein Name': [],
            'Node GO': [],
            'Node Organisme': [],
            'Node Genes names': [],
            'Node Labeled': [],
            'Node Label suggestion': [],
            'Node Hierarchy': []
            }
    return data

def get_pie_values():
    a=mongodb.labelStat(db_cm)[0]
    b=mongodb.labelStat(db_cm)[1]
    return [a,b]


def get_neighbours(entry):
    return neo.getNeighbors(entry)



def fill_table(entry, data, k,f):
    if(f==0):
        print(entry)
        list1, list2, list3, list4, list5, list6, =  mongodb.nameSearch(entry,db_cm)
    else :
        list1, list2, list3, list4, list5, list6, = mongodb.entrySearch(entry,db_cm)
    for i in range(len(list1)):
        data['Node Entry Name'].append(list1[i])
        data['Node Protein Name'].append(list2[i])
        data['Node GO'].append(list5[i])
        data['Node Organisme'].append(list3[i])
        data['Node Genes names'].append(list4[i])
        data['Node Labeled'].append(list6[i])
        if(list6[i]!='Labeled'):
            data['Node Label suggestion'].append(neo.label(list1[i]))
        else:
            data['Node Label suggestion'].append('')
        data['Node Hierarchy'].append(k)
    #print(list1[0])
    return list1[0]


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    pie_values = get_pie_values()
    data = get_data()
    if request.method == 'POST':
        entry_name=request.form['name']

        protein=request.form['email']
        #print(entry_name, entry, protein)
        #password=request.form['password']
        # data['Entry Name'].append(name)
        # data['Entry'].append(email)
        # pie_values = [1,6]
        # data['Protein Name'].append(surname)
        # data['Qualification'].append(surname)
        # nodes_list = get_node(5)
        # for e in nodes_list:
        #     n, p, d = e[0]
        #     n1, p1, d1 = e[1]
        #     n2, p2, d2 = e[2]
        #     data['Node Entry Name'].append(n)
        #     data['Node Protein Name'].append(p)
        #     data['Node GO'].append(d)
        #     data['Node Organisme'].append(n1)
        #     data['Node Genes names'].append(p1)
        #     data['Node Labeled'].append(d1)
        #     data['Node Label suggestion'].append(n2)
        #     data['Node Hierarchy'].append(p2)
        l=[]
        if(len(entry_name)>0):
            l = fill_table(entry_name, data, 0, 1)

        else:
            l=fill_table(protein, data, 0, 0)
        neighbours = get_neighbours(l)
        #print(len(neighbours))
        for i in range(len(neighbours)):
            fill_table(neighbours[i], data, str(0)+str(i) ,1)
            neighbours2 = get_neighbours(neighbours[i])
            #print(len(neighbours))
            for j in range(len(neighbours2)):
                fill_table(neighbours2[j], data, str(0)+str(i) + str(j),1)

    # if form.validate():
    #     write_to_disk(entry_name,  protein)
    #     flash('Results for: {} {}'.format(entry_name, protein))
    #
    # else:
    #     flash('Results for: {} {}'.format(entry_name, protein))

    pie_labels = [labels[i] for i in range(len(pie_values))]
    females = pd.DataFrame(data)
    titles = ['na', 'Female surfers', 'Male surfers']
    return render_template('index.html', data=[females.to_html(classes='female')], titles=titles,form=form,title='Bitcoin Monthly Price in USD', max=17000,
                           set=zip(pie_values, pie_labels, colors))

if __name__ == "__main__":
    client = mongodb.pymongo.MongoClient('localhost', 27017)
    db = client['DataBank']
    collection_name = 'Protein'
    db_cm = db[collection_name]
    filepath1 = 'Ressources/Ressources_reviewed.csv'
    filepath2 = 'Ressources/Ressources_unreviewed.csv'
    #mongodb.import_csvfile(filepath1, filepath2,db_cm)
    app.run()