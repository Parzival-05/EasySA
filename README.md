# EasySA

<a id="readme-top"></a>

<ol>
<li>
    <a href="#русский-язык">Русский язык</a>
</li>
<li>
    <a href="#English">English</a>
</li>
</ol>

## Русский язык

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <h3 align="center">EasySA</h3>

  <p align="center">
    Приложение, обернутое в Telegram, для автоматической публикации информации о начале стримов в личные медиа
стримеров (социальные сети, мессенджеры, ...).
  </p>
  <p align="center">
    <a href="#Начните-автопостинг">Использование</a>
    ·
    <a href="https://github.com/Parzival-05/EasySA/issues/new?labels=bug&template=bug-report---.md">Сообщить об ошибке</a>
    ·
    <a href="https://github.com/Parzival-05/EasySA/issues/new?labels=enhancement&template=feature-request---.md">Запросить функцию</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->

<details>
  <summary>Содержание</summary>
  <ol>
    <li>
      <a href="#о-проекте">О проекте</a>
      <ul>
        <li><a href="#инструменты-для-работы">Инструменты для работы</a></li>
      </ul>
    </li>
    <li>
      <a href="#начало-работы">Начало работы</a>
      <ul>
        <li><a href="#Инструкции-по-запуску-и-настройке-для-Windows">Инструкции по запуску для Windows</a></li>
        <li><a href="#Интеграция-с-Twitch">Интеграция с Twitch</a></li>
      </ul>
    </li>
    <li><a href="#Начните-автопостинг">Начните автопостинг</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## О проекте

Приложение, обернутое в Telegram, для автоматической публикации информации о начале стримов в личные медиа
стримеров (социальные сети, мессенджеры, ...). При обнаружении активности стримера, настроенные посты сразу публикуются
в указанных пользователем медиа.

В настоящее время приложение поддерживает следующие стриминг платформы:

- Twitch

И следующие медиа платформы:

- Telegram каналы
- Discord каналы

<p align="right">(<a href="#readme-top">наверх</a>)</p>

<!-- BUILT WITH -->

### Инструменты для работы

* [Python](https://www.python.org/downloads/)

<p align="right">(<a href="#readme-top">наверх</a>)</p>

<!-- GETTING STARTED -->

## Начало работы

<!-- WINDOWS STARTUP -->

### Инструкции по запуску и настройке для Windows

1. `git clone https://github.com/Parzival-05/EasySA`
2. `cd EasySA`
3. Создать venv:
    1. `python -m pip install virtualenv`
    2. `python -m virtualenv .venv`
    3. `.venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. `alembic upgrade head`
6. Получить токен вашего телеграм-бота с помощью [BotFather](https://t.me/BotFather). Создайте и заполните файл .env:
    ```
   BOT_TOKEN_API = '...'
    ```
7. Для интеграции со стриминг платформами необходимо ввести некоторые учетные данные
   в файл .env (см. ниже как).
8. Заполните поле `ADMIN_IDS` в `.env`: введите ID, разделенные запятыми, из https://t.me/getmyid_bot.
9. Запуск: `python main.py` (возможно, потребуются права администратора).

### Интеграция с Twitch

Нужно получить client id и client secret.

1. Зарегистрируйте свое приложение по инструкции: https://twitch4j.github.io/rest-helix/:
    1. Нужно будет включить авторизацию через OAuth2.
    2. Укажите в поле "OAuth Redirect URL" "http://localhost", не нажимая "Добавить".
    3. Выберите любую категорию приложения.
    4. Нажмите "Создать".
2. В консоли (https://dev.twitch.tv/console) выберите свое приложение, скопируйте client id и client secret.
3. Заполните файл .env:
    ```
    TWITCH_CLIENT_ID = '...'
    TWITCH_CLIENT_SECRET = '...'
    ```

<p align="right">(<a href="#readme-top">наверх</a>)</p>

## Начните автопостинг

[Figma](https://www.figma.com/board/gYlJvQQHxwGYMzcyeEROvH/EasySA?node-id=0-1&node-type=canvas&t=b1IHKMi7wQyAwBPE-0)
<p align="right">(<a href="#readme-top">наверх</a>)</p>

## English

<br />
<div align="center">
  <h3 align="center">EasySA</h3>

  <p align="center">
    Telegram-wrapped app for auto-posting information about the beginning of streams to streamers' personal media
(social networks, messengers, ...)
  </p>
  <p align="center">
    <a href="https://github.com/Parzival-05/EasySA/">View usage</a>
    ·
    <a href="https://github.com/Parzival-05/EasySA/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Parzival-05/EasySA/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#Windows-specific-startup-instructions">Windows-specific startup instructions</a></li>
        <li><a href="#Twitch-integration">Twitch integration</a></li>
      </ul>
    </li>
    <li><a href="#start-posting">Start posting</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About The Project

Telegram-wrapped app for auto-posting information about the beginning of streams to streamers' personal media
(social networks, messengers, ...). When streamer activity is detected, customized posts are immediately published to
the media specified by the user.

The app currently supports the following streaming platforms:

- Twitch

And the following media platforms:

- Telegram channels
- Discord channels

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- BUILT WITH -->

### Built With

* [Python](https://www.python.org/downloads/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

<!-- WINDOWS STARTUP -->

### Windows-specific startup instructions

1. `git clone https://github.com/Parzival-05/EasySA`
2. `cd EasySA`
3. Create venv:
    1. `python -m pip install virtualenv`
    2. `python -m virtualenv .venv`
    3. `.venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. `alembic upgrade head`
6. Get token of your telegram bot with [BotFather](https://t.me/BotFather). Create and fill the .env file:
    ```env
    BOT_TOKEN_API = '...'
    ```
7. To integrate with streaming platforms, you first need to enter some credentials into the env file (see below how to).
8. Fill the `ADMIN_IDS` field in `.env`: enter the comma-separated IDs from https://t.me/getmyid_bot.
9. Running: `python main.py` (you may need administrator rights).

### Twitch integration

See how to get twitch credentials to use the Twitch API here: https://twitch4j.github.io/rest-helix/.
You need to get **client id** and **client secret** of app.

1. Register your app: follow the next steps: https://twitch4j.github.io/rest-helix/:
    1. You will need to enable authorization via OAuth2.
    2. Specify the "OAuth Redirect URL" field with "http://localhost", without clicking "Add".
    3. Select any category of app.
    4. Click "Submit".
2. In [the console](https://dev.twitch.tv/console) select your app and copy the **client id** and **client secret**.
3. Fill the .env file:
    ```env
    TWITCH_CLIENT_ID = '...'
    TWITCH_CLIENT_SECRET = '...'
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Start posting

❗Only the Russian-language interface is supported for now❗

[See Figma](https://www.figma.com/board/gYlJvQQHxwGYMzcyeEROvH/EasySA?node-id=0-1&node-type=canvas&t=b1IHKMi7wQyAwBPE-0)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

### Features:

- [ ] Support of stream platforms
    - [x] Twitch
    - [ ] Youtube
- [ ] Support of media platforms
    - [x] Telegram channels
    - [x] Discord channels
    - [ ] VK
- [ ] Multi-language Support
    - [x] Russian
    - [ ] English

See the [open issues](https://github.com/Parzival-05/EasySA/issues) for a full list of proposed features (
and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->

## Contact

David - parzivalwasd@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>
