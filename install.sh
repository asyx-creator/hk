#!/bin/bash

# Проверка на root права
if [ "$EUID" -ne 0 ]; then
  whiptail --title "ERROR / ОШИБКА" --fb --msgbox "Запустите инсталлер через sudo!\n(sudo ./install.sh)" 10 50
  exit 1
fi

# Настраиваем сине-красную цветовую гамму для whiptail
export NEWT_COLORS='
  root=blue,blue
  window=blue,lightgray
  border=blue,lightgray
  textbox=blue,lightgray
  button=white,red
  actbutton=white,blue
  checkbox=blue,lightgray
  entry=blue,lightgray
  title=red,lightgray
'

# Приветственное окно
whiptail --title "HAIKU OS LANG INSTALLER" --fb \
--yesno "Добро пожаловать в установщик языка Haiku!\n\nХотите продолжить установку?" 12 55

if [ $? -ne 0 ]; then
    whiptail --title "CANCEL" --fb --msgbox "Установка отменена пользователем." 8 45
    exit 0
fi

# Процесс установки компонентов
(
echo 20 ; sleep 0.5
if [ -f /etc/fedora-release ]; then
    dnf install -y python3-tkinter > /dev/null 2>&1
elif [ -f /etc/gentoo-release ]; then
    emerge --ask=n dev-lang/tk > /dev/null 2>&1
elif [ -d /etc/guix ] || command -v guix &> /dev/null; then
    # GNU Guix поддержка
    guix install python-tkinter > /dev/null 2>&1
elif [ -f /etc/slackware-version ]; then
    echo "Slackware detected" > /dev/null
fi

echo 60 ; sleep 0.5
# 2. Проверка существования основного файла
if [ ! -f "lumi.py" ]; then
    exit 2
fi

cp lumi.py /usr/local/bin/haiku
chmod +x /usr/local/bin/haiku
sed -i '1s/^/#!\/usr\/bin\/env python3\n/' /usr/local/bin/haiku

echo 100 ; sleep 0.5
) | whiptail --title "Установка Haiku" --fb --gauge "Пожалуйста, подождите...\nНастройка компонентов системы и зависимостей." 8 50 0

# Ловим ошибку отсутствия файла
if [ $? -eq 2 ]; then
    whiptail --title "ОШИБКА" --fb --msgbox "Критическая ошибка: Файл lumi.py не найден в текущей папке!" 10 50
    exit 1
fi

# Финальное окно успеха
whiptail --title "УСПЕХ / SUCCESS" --fb \
--msgbox "Язык Haiku успешно установлен в систему!\n\nТеперь вам доступны команды:\n  haiku run файл.haiku\n  haiku build файл.haiku" 12 55
