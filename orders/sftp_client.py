import paramiko
from django.core.files.base import ContentFile

from config import settings


def upload_to_sftp(file, temp_dir, filename):

    # Установка соединения с SFTP-сервером
    transport = paramiko.Transport((settings.HOST, settings.PORT))
    transport.connect(username=settings.FTP_LOGIN, password=settings.FTP_PASS)

    sftp = paramiko.SFTPClient.from_transport(transport)

    remote_path = settings.UPLOAD_FOLDER + temp_dir

    # Загружаем файл на сервер
    with sftp.file(remote_path, 'wb') as sftp_file:
        sftp_file.write(file.read())

    sftp.close()
    transport.close()

