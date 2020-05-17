import mysql.connector


class Profile:
    def __init__(self, id, name, lastname, gender, age, address, phone, aadhar, mail, imgBlobText):
        self.name = name;
        self.lastname = lastname;
        self.gender = gender;
        self.age = age;
        self.address = address;
        self.phone = phone;
        self.aadhar = aadhar;
        self.mail = mail;
        self.id = id;
        self.imgBlobText = imgBlobText;


class ProfileManager:

    def createProfile(self, p):
        self.connection = self.__open()
        self.cursor = self.connection.cursor()
        sql = "INSERT INTO profile(id,name, lastname,gender, age, address, phone, aadhar, mail, picture)" \
              "VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')" \
            .format(p.id, p.name, p.lastname, p.gender, p.age, p.address, p.phone, p.aadhar, p.mail, p.imgBlobText)

        self.cursor.execute(sql);
        self.connection.commit();
        self.connection = self.__close();

    def updateProfile(self,name,  age, mail):
        self.connection = self.__open()
        self.cursor = self.connection.cursor()
        sql = "update profile set age={} where mail='{}'".format(age, mail);
        print("sql:" + sql)
        self.cursor.execute(sql);
        self.connection.commit();
        self.connection = self.__close()

    def deleteProfile(self, id):
        self.connection = self.__open()
        self.cursor = self.connection.cursor()
        sql = "DELETE FROM profile where id='{}'".format(id);

        self.cursor.execute(sql);
        self.connection.commit();
        self.connection = self.__close()

    def select(self, p):
        self.connection = self.__open();
        self.cursor = self.connection.cursor();
        sql = "SELECT name ,lastname,gender,age,address,phone, aadhar,mail from profile where id='{}'".format(p.id);

        self.cursor.execute(sql)
        row = self.cursor.fetchone()

        self.connection = self.__close()
        return row

    def listall(self, num):
        self.connection = self.__open()
        self.cursor = self.connection.cursor()
        # sql="SELECT * from profile LIMIT 0,{}".format(num);
        sql = "SELECT id,name,lastname,gender,age,address,phone, aadhar,mail,picture from profile LIMIT 0,{}".format(
            num);
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        self.connection = self.__close()
        return rows

    def __open(self):
        self.connection = mysql.connector.connect(host='127.0.0.1', user='root', passwd='root', database='chennai')
        return self.connection

        # def help(self):
        self.insert(p)
        self.__open

    def __close(self):
        self.connection.close()


# p=Profile('ishu')
# p=Profile("dhivya","T","female",34,"first new street",9999999999,"77878787","jjj@hotmail.com")
# manager = ProfileManager();
# manager.createProfile(p)
# manager.deleteProfile("ishu@gmail.com");
# manager.updateProfile(55,"sivahari@gmail.com");

if __name__ == '__main__':
    pm = ProfileManager();
    pm.listall(2);
