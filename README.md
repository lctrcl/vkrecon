**tl;dr**
(ENG/RUS)

Vkontakte company employees and secondary connections enumerator

Скрипт для определения сотрудников компании и пересечения взаимных друзей из вконтакте

## About

This is a python script for reconnaissance to enumerate vkontakte users which has certain company set in the profile. Moreover, it looks into mutual friends and compares sets to investigate further connections. This will help you find secondary connections between users and with some luck find more employees. 

Скрипт для определения пользователей вконтакте, у которых в профиле указана определённая компания. Опционально может определять пересечения взаимных друзей, затем взаимных друзей друзей, определяя возможных сотрудников, у которых не указана компания. 



## Usage

    git clone https://github.com/lctrcl/vkrecon
    pip install -r requirements.txt

You can set username, password and company in the separate `config.py` file:

    login = 'ololo@vk.com'
    password = '1q2w3e4r'
    company = 'VK'

No options required when running:

    python vkrecon.py


*TAGS: osint, python, vkontakte, enumeration, recon, reconnaissance*
