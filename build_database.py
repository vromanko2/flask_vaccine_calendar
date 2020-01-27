import os
from models import db, Table, Data, Contraindication, Vaccines
from run import create_app

# app.app_context().push()

app = create_app("config")

vaccines = ['Туберкульоз', 'Поліомієліт', 'Дифтерія', 'АКДП', 'АДП', 'КПК', 'Гепатит В', 'Хіб-інфекція']

vaccines_ = [
    {
        'title': 'Туберкульоз',
        'contraindications': [''],
        'periodicity': 0,
        'by_health': False
    },
    {
        'title': 'Поліомієліт',
        'contraindications': [''],
        'periodicity': 1,
        'by_health': False

    },
    {
        'title': 'Дифтерія',
        'contraindications': [''],
        'periodicity': 0,
        'by_health': False
    },
    {
        'title': 'АКДП',
        'contraindications': [''],
        'periodicity': 1,
        'by_health': False
    },
    {
        'title': 'АДП',
        'contraindications': [''],
        'periodicity': 1,
        'by_health': False
    },
    {
        'title': 'КПК',
        'contraindications': [''],
        'periodicity': 1,
        'by_health': False
    },
    {
        'title': 'Гепатит В',
        'contraindications': ['Хронічні захворювання печінки', 'Трансплантація органів', 'Гемодіаліз',
                              'Довготривалі переливання донорської крові або її препаратів',
                              'Планові оперативні втручання'],
        'periodicity': 1,
        'by_health': False
    },
    {
        'title': 'Хіб-інфекція',
        'contraindications': ['Первинні імунодефіцити', 'Хронічні захворювання легень', 'Лімфома',
                              'Множинна мієлома', 'Лейкемія', 'хвороба Ходжкіна', 'Транслантація кісткового мозку',
                              'Трансплантація органів'],
        'periodicity': 1,
        'by_health': False
    },
    {
        'title': 'Грип',
        'contraindications': ['Первинні імунодефіцити', 'Цукровий діабет', 'Бронхіальна астма', 'ВІЛ-інфекція',
                              'Хронічні захворювання печінки', 'Ураження нирок', 'Транслантація кісткового мозку',
                              'Хронічні захворювання легень', 'Хронічні ураження серцево-судинної системи'],
        'periodicity': 12,
        'by_health': True
    },
    {
        'title': 'Пневмококова інфекція',
        'contraindications': ['ВІЛ-інфекція', 'Ураження нирок', 'Первинні імунодефіцити', 'Цукровий Діабет 1',
                              'Бронхіальна астма', 'Функціональна чи анатомічна аспленія',
                              'Хронічні захворювання печінки', 'Назальна лікворея', 'Хронічні захворювання легень',
                              'Туберкульоз', 'Хронічні ураження серцево-судинної системи', 'Лімфома',
                              'Множинна мієлома', 'Лейкемія', 'хвороба Ходжкіна', 'Транслантація кісткового мозку',
                              'Імуносупресивна гормональна терапія', 'Трансплантація органів'],
        'periodicity': 2,
        'by_health': True
    },
    {
        'title': 'Хіб-інфекції',
        'contraindications': ['Первинні імунодефіцити', 'Хронічні захворювання легень', 'Лімфома',
                              'Множинна мієлома', 'Лейкемія', 'хвороба Ходжкіна', 'Транслантація кісткового мозку',
                              'Трансплантація органів'],
        'periodicity': 3,
        'by_health': True
    },
    {
        'title': 'Менінгококова інфекція',
        'contraindications': ['Функціональна чи анатомічна аспленія', 'Пропердин', 'Фактор В',
                              'Комплемент С1, С2, С3, С4, С5-С9'],
        'periodicity': 3,
        'by_health': True
    },
    {
        'title': 'Гепатит А',
        'contraindications': ['Хронічні захворювання печінки', 'Трансплантація печінки'],
        'periodicity': 6,
        'by_health': True
    }

]

vac_dict = {}

if os.path.exists("app.sqlite"):
    os.remove("app.sqlite")

# Create the database
# with app.app_context():
#     db.create_all()

# for vac_name in vaccines:
#     vaccine = Vaccines(vac_name, 1)
#     vac_dict[vac_name] = vaccine
#     db.session.add(vaccine)
# db.session.commit()


def build_database():
    db.create_all()
    contraindications = []

    for vacc in vaccines_:
        for cont in vacc['contraindications']:
            contraindications.append(Contraindication(cont))
        vaccine = Vaccines(vacc['title'], 1, contraindications, vacc['by_health'], vacc['periodicity'])
        vac_dict[vacc['title']] = vaccine
        contraindications = []
        db.session.add(vaccine)
    db.session.commit()

    data1 = Data(2, [vac_dict['Гепатит В'], vac_dict['АКДП'], vac_dict['Поліомієліт'], vac_dict['Хіб-інфекція']])
    db.session.add(data1)
    data2 = Data(4, [vac_dict['АКДП'], vac_dict['Поліомієліт'], vac_dict['Хіб-інфекція']])
    db.session.add(data2)
    data3 = Data(6, [vac_dict['Гепатит В'], vac_dict['АКДП'], vac_dict['Поліомієліт']])
    db.session.add(data3)
    data4 = Data(12, [vac_dict['Хіб-інфекція'], vac_dict['КПК']])
    db.session.add(data4)
    data5 = Data(18, [vac_dict['АКДП'], vac_dict['Поліомієліт']])
    db.session.add(data5)
    data6 = Data(72, [vac_dict['АДП'], vac_dict['Поліомієліт'], vac_dict['КПК']])
    db.session.add(data6)
    data7 = Data(168, [vac_dict['Поліомієліт']])
    db.session.add(data7)
    data8 = Data(192, [vac_dict['АДП']])
    db.session.add(data8)

    data9 = Data(6, [vac_dict['Грип']])
    db.session.add(data9)
    data10 = Data(0, [vac_dict['Пневмококова інфекція']])
    db.session.add(data10)
    data11 = Data(0, [vac_dict['Хіб-інфекції']])
    db.session.add(data11)
    data12 = Data(24, [vac_dict['Менінгококова інфекція']])
    db.session.add(data12)
    data13 = Data(12, [vac_dict['Гепатит А']])
    db.session.add(data13)

    table = Table("calendar of vaccination",
                  [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13])
    db.session.add(table)

    table.data = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13]

    db.session.commit()
    print()
    print()
    for data_item in Data.query.all():
        print(data_item.age_in_months, end=" = ")
        for vacine in data_item.vaccines:
            print(vacine.name, ":", vacine.dose, " by health: ", vacine.by_health)
            for contraindication in vacine.contraindications:
                print(" [", contraindication.title, end="] ")

            print()
        print()
        print()


with app.app_context():
    build_database()
