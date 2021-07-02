import requests
from bs4 import BeautifulSoup

client = requests.session()
main_link = "https://change.org"
client.get(main_link)


# LOGIN
def login(my_mail, my_passwd):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://www.change.org/',
        'Content-Type': 'application/json',
        'X-CSRF-Token': 'c3c9cc8b0c00f855c78426d3fc7c00ff',
        'X-Requested-With': 'jquery',
        'Origin': 'https://www.change.org',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"validateAs":"login","email":"' + my_mail + '","password":"' + my_passwd + '"}'

    cookies = client.cookies.get_dict()

    # temp_var = dict()
    # temp_var.__str__()

    response = client.post('https://www.change.org/api-proxy/-/users/login_by_credentials', headers=headers,
                           cookies=cookies, data=data)

    if 200 <= response.status_code < 300:
        print("Login completed successfully")
        return 1
    print("Login error. Status code " + response.status_code.__str__())
    return 0


# USER INFO
def user_info():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://www.change.org/',
        'Content-Type': 'application/json',
        'X-CSRF-Token': 'c3c9cc8b0c00f855c78426d3fc7c00ff',
        'X-Requested-With': 'jquery',
        'Origin': 'https://www.change.org',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    cookies = client.cookies.get_dict()

    # GET INFO
    response = client.get(main_link, headers=headers, cookies=cookies)
    if 100 <= response.status_code < 200 and 300 <= response.status_code:
        print("Information retrieval error. Status code " + response.status_code.__str__())
        return

    soup = BeautifulSoup(response.text, 'lxml')
    block = soup.find('script', id="clientData")

    # PARSING
    user_inf = block.string[block.string.find("currentUser"):block.string.find("account_info")]

    id_ = user_inf[19:(user_inf.find("email") - 2)]
    print("id:", id_)

    mail = user_inf[(user_inf.find("email") + 8): (user_inf.find("first_name") - 3)]
    print("email:", mail)

    first_name = user_inf[(user_inf.find("first_name") + 13): (user_inf.find("last_name") - 3)]
    print("first name:", first_name)

    last_name = user_inf[(user_inf.find("last_name") + 12): (user_inf.find("display_name") - 3)]
    print("last name:", last_name)

    location = user_inf[(user_inf.find("formatted_location_string") + 28): (user_inf.find("locale") - 3)]
    print("location:", location)

    description = user_inf[(user_inf.find("description") + 14): (user_inf.find("roles") - 3)]
    print("description:", description)

    link_to_profile = user_inf[(user_inf.find("slug") + 7): (user_inf.find("uuid") - 3)]
    print("link to profile:", link_to_profile)

    website = user_inf[(user_inf.find("website") + 10): (user_inf.find("address") - 3)]
    print("website:", website)

    address = user_inf[(user_inf.find("address") + 10): (user_inf.find("postal_code") - 3)]
    print("address:", address)

    phone_number = user_inf[(user_inf.find("phone_number") + 15): (user_inf.find("congressional_district") - 3)]
    print("phone number:", phone_number)


# LOGOUT
def logout():
    client.cookies.clear()
    cookies = requests.get(main_link).cookies.get_dict()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://www.change.org/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }

    params = (
        ('redirect_to', '/'),
    )
    client.close()
    response = requests.get('https://www.change.org/logout', headers=headers, params=params, cookies=cookies)
    if 100 <= response.status_code < 200 and 300 <= response.status_code:
        print("Logout error. Status code " + response.status_code.__str__())
        return

    response = requests.get('https://www.change.org/', headers=headers, cookies=cookies)
    if 100 <= response.status_code < 200 and 300 <= response.status_code:
        print("Logout error. Status code " + response.status_code.__str__())
        return

    print("Logout successful")
    return 0


def petition_search(title):
    link = 'https://www.change.org/search?q=' + title

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }

    cli = requests.session()
    cli.get(main_link)

    cookies = cli.cookies.get_dict()

    response = requests.get(link, headers=headers, cookies=cookies)
    if 100 <= response.status_code < 200 and 300 <= response.status_code:
        print("Information retrieval error. Status code " + response.status_code.__str__())
        return 0

    soup = BeautifulSoup(response.text, 'lxml')

    block = soup.find('div', class_="search-result")
    if block is None:
        print("No result")
        return
    block = block.find('a').get('href')
    print(main_link + block)


def switch(value, flag):
    if value == '1':
        print("Input email:")
        my_mail = input()
        print("Input password:")
        my_passwd = input()
        flag = login(my_mail, my_passwd)
    if value == '2':
        if flag == 1:
            user_info()
        else:
            print("You need login")
    if value == '3':
        print("Input title:")
        title = input()
        petition_search(title)
    if value == '4':
        flag = logout()
    if value == '5':
        exit()
    return flag


is_login = 0
while True:
    print("Select an action:\n"
          "1. Login\n"
          "2. User's info\n"
          "3. Petition search\n"
          "4. Logout\n"
          "5. Exit")
    choose = input()
    is_login = switch(choose, is_login)
