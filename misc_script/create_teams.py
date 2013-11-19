'''
Created on 17-Jul-2012

@author: vijay
'''

from django.contrib.auth.models import Group, User

from users.models import Employees, Teams


def create_group():
    grp_mgr = Group(name='managers')
    grp_mgr.save()
    grp_lds = Group(name='leads')
    grp_lds.save()
    grp_eng = Group(name='engineer')
    grp_eng.save()


def create_users():
    user_dict = {
1: [1.0, u'Somashekarachari P', u'spachchipalu@vmware.com', u'ESX-Storage', 9742991397, 42550, u'Veg', u'XL', '', '', '', u'B+', '', u'Paul Kirubeker(pkirubaker@vmware.com)', u'Rani/Sudhish T (rani@vmware.com/sudhisht@vmware.com)'],
2: [2.0, u'Chakravarthi K K', u'chakravarthik@vmware.com', u'Storage- API', 9686192624, '', '', '', '', '', '', '', '', u'Prakash Gowda', u'Madhu(mgangadharan@vmware.com)'],
3: [3.0, u'Venkatesh Singh', u'prasadv@vmware.com', u'VC-UIFVT', 9663770702, '', u'Non-Veg', u'Medium', '', u'JP Nagar 5th Phase', u'No', u'AB+', '', u'Sthanu Subramanian [sthanu@vmware.com]', u'Swetha Nagarudraiah'],
4: [4.0, u'Sumalatha Kammula', u'skammula@vmware.com', u'ESX-Storage', 9986022524, 42552.0, u'Non-Veg', u'Large', '', u'Kammanhalli Manin Rd', u'No', u'O+', 9986032524.0, u'Ramesh Tammana [ramesht@vmware.com]', u'Sudhish P.T [sudhisht@vmware.com]/Abhshek Bagchi[abagchi@vmware.cm]/[Ramakrishna Kempaiah [ramakrishnak@vmware.com]'],
5: [5.0, u'Sajimon Narayanan', u'sajimonn@vmware.com', u'VC API', 9945410802, 42566, u'Non-Veg', u'Large', u'GM Palya', u'New Thippasandra', u'No', u'A+', 8095274717.0, u'Prakash Gowda', u'Gururaja Hegdal(ghegdal@vmware.com)'],
6: [6.0, u'Yogesh Chandra Pandey', u'ychandra@vmware.com', u'VC API', 8197416961, '', '', '', '', '', '', '', '', u'Prakash Gowda', u'Gururaja Hegdal(ghegdal@vmware.com)'],
7: [7.0, u'Vijay Kumar Bang', u'vijaybang@vmware.com', u'Tools', 9886761820, 42623, u'Veg', u'Medium', '', '', '', '', '', u'Manjunath H.N(madhusudan@vmware.com)', u'Siji Kuruvilla George ( sgeorge@vmware.com)'],
8: [8.0, u'Sembian', u'moorthys@vmware.com', u'ESX-Storage', 9900601931, 42556, u'Non-Veg', u'Large', '', '', u'No', '', 8973390929.0, u'Sandeep Arora (sarora@vmware.com)', u'Deeban/Sudhish T (dchakravarthy@vmware.com/sudhisht@vmware.com)'],
9: [9.0, u'Lakshmipathi', u'lakshmipathid@vmware.com', u'ESX-VC UI', 9986079641, 42551, u'Non-Veg', u'Medium', u'TC Palya ,KR Puram', u'TC Palya', u'Yes', u'B+', 9986049641.0, u'Sthanu Subramanian', u'Marichetty M S [marichetty@vmware.com]'],
10: [10.0, u'Hariprasad Manchi', '', u'VC API', 9945130386.0, u'NA', u'Veg', u'Medium', u'Vidyapeetha Circle', u'Srinivas Nagar', u'No', u'O+', '', u'Prakash Gowda', u'Ram Prakash (rpsoni@vmware.com)'],
11: [11.0, u'Naresh k', u'nareshk@vmware.com', u'VC API', 9886235509, '', '', '', u'Marathhalli Brigde', u'Marathhalli', '', '', '', u'Prakash Gowda', u'Madhu(mgangadharan@vmware.com)'],
 12: [12.0, u'Subash Kumar Parida', u'sparida@vmware.com', u'VC API', 9742810393, 42598.0, u'Non-Veg', u'Large', u'N/A', u'Wilson Garden', u'No', '', '', u'Prakash Gowda', u'Gururaja Hegdal(ghegdal@vmware.com)'],
 13: [13.0, u'Puneet Khanna', u'pkhanna@vmware.com', u'Storage- API', 9538004119, '', '', '', '', '', '', '', '', u'Prakash Gowda', u'Madhu/Vinay (mgangadharan@vmware.com))'],
 14: [14.0, u'Dheeraj Rajendra', u'Did not find email', u'VC API', 8105529025, '', '', '', u'ITI Circle,near K R Puram', u'KR Puram', '', '', '', u'Prakash Gowda', u'Ram(rpsoni@vmware.com)'],
 15: [15.0, u'Shubha A C', u'shubhac@vmware.com', u'RMT', 9740466889.0, 42592, u'Veg', u'XL', '', u'Jp nagar 2nd phase', u'No', u'O+', 9741807950.0, u'Vipul Dhondiyal(vipuld@vmware.com)', u'Siva Sankar reddy B / Sudarshan Shetty(sushetty@vmware.com)'],
 16: [16.0, u'Satheesh Kannan J', u'kannans@vmware.com', u'ESX-PDP', 9620074091, 42617, u'Non-Veg', u'Large', u'N/A', u'Arekere', u'No', u'O+', 9944359090.0, u'Prakash narayana', u'Rahul Torvi(rahul@vmware.com)/Nitin Krishnan(nkrishnan@vmware.com)'],
 17: [17.0, u'Lija Chandran', u'lchandran@vmware.com', u'PDP', 9483103009, '', '', '', u'Maruthi Nagar,Madiwala', u'Madivala', '', '', '', u'Prakash Narayana[pnarayan@vmware.com]', u'Rahul Torvi [rahul@vmware.com]/ Nithin Krishnan [nkrishnan@vmware.com]'],
 18: [18.0, u'Chandramauli Priya Mohapatra', u'pmohapatra@vmware.com', u'RMT', 9739008884, 42609, u'Non-Veg', u'Large', u'Bellandur', u'Bellandur,Outer ring road', u'Yes', u'B+', 9620931608.0, u'Vipul Dhondiyal', u'Sudarshan Shetty [sushetty@vmware.com]'],
 19: [19.0, u'Ranjit Ashtekar', u'rashtekar@vmware.com', u'ESX-Storage', 9845814617, '', '', '', '', '', '', '', '', u'Sandeep Arora', u'Rajavardhan Bhat (Rajavardhan@vmware.com)'],
 20: [20.0, u'Kalyan Goutham', u'kgoutham@vmware.com', u'VC API', 9686083910, 42609, u'Veg', u'Large', u'Vidhyaranyapura', '', u'yes', u'A+', 9686083910.0, u'Prakash Gowda', u'Madhu(mgangadharan@vmware.com)'],
 21: [21.0, u'Abhisek Roy', u'abhisekroy@vmware.com', u'VC API', 9008114363, '', '', '', u'Hope Farm', u'Kadugodi', '', u'O+', '', u'Prakash Gowda', u'Ram(rpsoni@vmware.com'],
 22: [22.0, u'Vijaya K', u'vijayak@vmware.com', u'VC API', u'8494950009', '', '', '', u'BTM 2nd Stage', u'BTM Layout', '', u'O-', 9164543999.0, u'Prakash Gowda', u'Ram(rpsoni@vmware.com'],
 23: [23.0, u'Krithee', u'kirtheek@vmware.com', u'VC API', 9886735404, '', u'Veg', u'XL', u'N/A', u'Indiranagar', u'No', u'B-', 9886590226.0, u'Prakash Gowda', u'Ram(rpsoni@vmware.com'],
 25: [25.0, u'Solomon', u'sprasadb@vmware.com', u'PDP', 9663373535, '', '', '', u'Banasawadi', '', '', '', '', u'Prakash Narayana[pnarayan@vmware.com]', u'Rahul Torvi [rahul@vmware.com]/ Nithin Krishnan [nkrishnan@vmware.com]'],
 26: [26.0, u'Jasmeet Karir', u'jkarir@vmware.com', u'ESX-Storage ST', u'9535626251', 42329.0, u'Non-Veg', u'XL', '', '', u'No', u'O+', '', u'Sandeep Arora (sarora@vmware.com)', u'Sudhish P.T.[Sudhisht@vmware.com]/Deeban chakravarthy[dchakravarthy@vmware.com]'],
 27: [27.0, u'Vijayasri D', u'dvijayasri@vmware.com', u'ESX-Storage ST', u'8123898508', '', '', '', u'Marathahalli', u'Munnekolala', u'No', u'b+', '', u'Sandeep Arora (sarora@vmware.com)', u'Sudhish P.T.[Sudhisht@vmware.com]/Deeban chakravarthy[dchakravarthy@vmware.com]'],
 28: [28.0, u'Rikesh S', u'rikeshs@vmware.com', u'ESX-Storage ST', 9742824812, '', u'Veg', u'XL', u'N/A', u'Telecom Colony,My road', u'No', u'A+', 9742824812.0, u'Sandeep Arora (sarora@vmware.com)', u'Sudhish P.T.[Sudhisht@vmware.com]'],
 29: [29.0, u'Somashekhar D M', u'somashekharm@vmware.com', u'ESX-ST', 9940420099, '', '', '', '', u'Anjanapur', u'Yes', '', '', u'Sandeep Arora (sarora@vmware.com)', u'Sudhish P.T.[Sudhisht@vmware.com]'],
 30: [30.0, u'Amit Shahane', u'ashahane@vmware.com', u'', u'09686899118', u'42670', u'Non-Veg', u'Large', u'N/A', u'JayaNager', u'No', u'O-Rh Positive', u'09822090197', u'Sandeep Arora (sarora@vmware.com)', u'Sudhish P.T.[Sudhisht@vmware.com]'],
 31: [31.0, u'komal kapoor', u'kkapoor@vmware.com', u'VCPDP', u'09916411169', '', '', '', u'btm', u'btm', u'yes', u'B+', '', '', ''],
 32: [32.0, u'Vishwanath Sagar M', u'vvishwanathmsag@vmware.com', u'ESX-VC UIFVT', 9900025737, 42609, u'Non-Veg', u'XL', u'Kundanahalli Gate', u'Kundanahalli', u'Yes', u'B+', '', u'Sthanu Subramanian [sthanu@vmware.com]', ''],
 33: [33.0, u'Kiran Kumar Grandhi', u'kgrandhi@vmware.com', u'ESX-Storage ST', u'9916490889', 42599, u'Veg', u'Medium', u'Marathahalli, Spice garden', u'Marathahalli', u'Yes', u'B+', 9985243043.0, u'Sandeep Arora (sarora@vmware.com)', u'Sudhish P.T.[Sudhisht@vmware.com]'],
 34: [34.0, u'Pashupathinath Cheela', u'pcheela@vmware.com', u'ESX-PDP', u'9008003342', 42551, u'Veg', u'XL', '', u'Bellandur', u'No', u'O+', 919440690588.0, u'Prakash Narayana[pnarayan@vmware.com]', ''],
 35: [35.0, u'Avinash', u'aprem@vmware.com', u'RMT', u'9880837984', '', u'non-veg', u'XL', u'btm', '', '', '', '', '', ''],
36: [36.0, u'Prakash Hallalli', u'phallali@vmware.com', '', 8050740267, 42599, u'Non-Veg', u'Medium', u'Vijayanagar', u'Vijayanagar', u'Yes', u'B-', '', u'Sandeep Arora (sarora@vmware.com)', u'Sudhish P.T.[Sudhisht@vmware.com]'],
37: [37.0, u'Samir Swarup', u'swarups@vmware.com', u'VC API', 9535788227, '', u'Non-Veg', u'Medium', u'BTM 2nd Stage', u'BTM Layout', '', '', 9451881829.0, u'Prakash Gowda', u'Ram(rpsoni@vmware.com'],
38: [38.0, u'Vinayaga Moorthy', u'vmoorthy@vmware.com', u'Tools', 9986070719, 42536, u'Non-Veg', u'XL', u'GM Palya', u'GM Palya', u'Yes', u'AB+', 9916957148.0, u'Pavan Kumar Arra (pavan@vmware.com)', u'Pavan Patwari (ppatwari@vmware.com)'],
39: [39.0, u'Pallavi Kolarkar', u'kolarkarp@vmware.com', u'ESX-Storage', 9980519732, 40607, u'Veg', u'Medium', u'N/A', u'Hulimavu, BG Road', u'No', u'O+', u'080-26586630', u'Srinivas K C (srinivas@vmware.com)', u'Lakshmi Gayatri(lgayatri@vmware.com)'],
40: [40.0, u'Dinesh Kumar Singh', u'dineshsingh@vmware.com', u'VC API', 8880567076, u'N/A', u'Non-Veg', u'Small', u'Mathikere', u'Mathikere', u'yes', u'O+', 7676784724.0, u'Prakash Gowda', u'Ram(rpsoni@vmware.com)']}
    team_names_list = []
    for id, val in user_dict.items():
        if val[2]:
            userObj = User(username=val[2],
                           first_name=val[1],
                           email=val[2],
                           is_active=True,
                           )
            userObj.set_password('login1-2')
            userObj.save()
            emp = Employees(user=userObj,
                            firstname=val[1],
                            tshirtsize=val[7],
                            food_preferance=val[6],
                            extension=val[5],
                            email=val[2],
                            emergencycontactno=val[12],
                            home_location=val[9])
            emp.save()
            team_names_list.append(val[3])
    for team in team_names_list:
        if team:
            obj, created = Teams.objects.get_or_create(lead=User.objects.get(username='ashahane@vmware.com'),
                                   teamname=team)

create_group()
create_users()

