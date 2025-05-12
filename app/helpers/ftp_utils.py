import ftplib
from fastapi import UploadFile, HTTPException

def upload_to_ftp(file: UploadFile) -> str:
    ftp_host = "localhost"
    ftp_user = "one"
    ftp_password = "123"
    ftp_directory = "/ftp/one/"

    try:
        with ftplib.FTP() as ftp:
            ftp.connect(ftp_host, 21)
            ftp.login(ftp_user, ftp_password)
            ftp.cwd(ftp_directory)

            server_filename = file.filename

            with file.file as f:
                ftp.storbinary(f"STOR {server_filename}", f)

            return f"{ftp_directory}{server_filename}"
    except ftplib.all_errors as e:
        raise HTTPException(status_code=500, detail=f"FTP error: {str(e)}")
