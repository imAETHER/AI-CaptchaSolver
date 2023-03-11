# AI-CaptchaSolver
Trained mostly with [Wick's](https://wickbot.com/) visual captchas that look like this:
<br>

![imagen](https://user-images.githubusercontent.com/36291026/224075087-648a65fd-6d75-4c0c-8c72-ad88f0ffc1f9.png)

Altough it can detect characters on other similar captchas

## Public API | [Documentation](https://yiffing.zone/api/docs) 
You are allowed to use this for whatever you want *within reason*, just dont send too many requests.

Example: `https://yiffing.zone/api/solve?captcha=https://cdn.discordapp.com/ephemeral-attachments/1082045093386670090/1083386900016025691/captcha.png&color=838ca6`

`captcha` is the url of the discord captcha, must begin with "`https://cdn.discordapp.com`".\
`color` **OPTIONAL**, its the color of the captcha's characters - Defaults to green if not provided\
(this also means that rainbow captchas wont work, but do let me know once they start doing those)

## Request model for bypass
If you have encountered a captcha that you wish to bypass using AI, you can make an issue with this info:
- Discord bot name
- A dataset of images/examples (just the images, no labels) in a zip file
- (optional) ways of making it easier to bypass/read
- (important) if the captcha case-sensitive
