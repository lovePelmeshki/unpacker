import os
import sys
import tarfile
import zipfile
import logging
import py7zr


# Логирование для удобства отладки
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def extract_7z(archive_path, extract_to):
    logger.debug(
        f"{__name__} : archive_path: {archive_path} : extract_to: {extract_to}"
    )

    archive_name = os.path.split(os.path.splitext(archive_path)[0])[1]
    extract_path = os.path.join(extract_to, archive_name)
    extract_path = ensure_unique_folder(extract_path)
    with py7zr.SevenZipFile(archive_path, mode="r") as archive:
        archive.extractall(extract_path)
        logger.debug(f"Successfully extracted {archive_path} to {extract_path}")


def extract_zip(archive_path, extract_to):
    logger.debug(f"extract_zip({archive_path}, {extract_to})")
    archive_name = os.path.split(os.path.splitext(archive_path)[0])[1]
    extract_path = os.path.join(extract_to, archive_name)
    extract_path = ensure_unique_folder(extract_path)
    with zipfile.ZipFile(archive_path, "r") as archive:
        archive.extractall(extract_path)
        logger.debug(f"Successfully extracted {archive_path} to {extract_path}")


def extract_tgz(archive_path, extract_to):
    logger.debug(f"extract_tgz({archive_path}, {extract_to})")

    archive_name = os.path.split(os.path.splitext(archive_path)[0])[1]
    extract_path = os.path.join(extract_to, archive_name)
    extract_path = ensure_unique_folder(extract_path)
    with tarfile.open(archive_path, "r:gz") as archive:
        archive.extractall(extract_path)
        logger.debug(f"Successfully extracted {archive_path} to {extract_path}")


def extract_tar_bz2(archive_path, extract_to):
    logger.debug(f"extract_tar_bz2({archive_path}, {extract_to})")

    archive_name = os.path.split(os.path.splitext(archive_path)[0])[1]
    extract_path = os.path.join(extract_to, archive_name)
    extract_path = ensure_unique_folder(extract_path)
    with tarfile.open(archive_path, "r:bz2") as archive:
        archive.extractall(extract_path)
        logger.debug(f"Successfully extracted {archive_path} to {extract_path}")


def extract_archive(archive_path, extract_to):

    final_exception = ""
    try:
        extract_7z(archive_path, extract_to)
    except Exception as e:
        logger.debug(f"7z extraction failed: {e}")
        final_exception = f"{archive_path}: 7z extraction failed: {e}"
        try:
            extract_zip(archive_path, extract_to)
            final_exception = ""
        except Exception as e:
            logger.debug(f"zip extraction failed: {e}")
            final_exception = f"{archive_path}: zip extraction failed: {e}"
            try:
                extract_tgz(archive_path, extract_to)
                final_exception = ""
            except Exception as e:
                logger.debug(f"tar extraction failed: {e}")
                final_exception = f"{archive_path}: tar extraction failed: {e}"
                try:
                    extract_tar_bz2(archive_path, extract_to)
                    final_exception = ""
                except Exception as e:
                    logger.debug(f"tar.bz2 extraction failed: {e}")
                    final_exception = f"{archive_path}: tar.bz2 extraction failed: {e}"
    finally:
        if final_exception != "":
            logger.warning(f"Extraction FAILED: {archive_path}")
            print(f"Extraction FAILED: {archive_path}. Reason: {final_exception}")


# проверить, существует ли папка с именем basefolder. Если да - изменить имя
def ensure_unique_folder(base_folder):
    if not os.path.exists(base_folder):
        return base_folder
    counter = 1
    new_folder = f"{base_folder}_{counter}"
    while os.path.exists(new_folder):
        counter += 1
        new_folder = f"{base_folder}_{counter}"
    return new_folder


# Предполагается, что extract_archive и ensure_unique_folder уже определены

def unpack_all_archives_in_folder(folder_path):
    """
    Рекурсивно проверяет каждую папку, ищет архивы и распаковывает их.
    """
    logger.debug(f"Checking folder for archives: {folder_path}")

    # Проходим по всем файлам и папкам в указанной директории
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Если найден архив, его нужно распаковать
            if is_archive(file_path):
                logger.debug(f"Found archive: {file_path}")

                try:
                    # Распаковываем архив
                    extract_archive(file_path, root)

                    # После распаковки, проверяем, есть ли вложенные архивы
                    new_extracted_folder = os.path.splitext(file_path)[0]
                    if os.path.isdir(new_extracted_folder):
                        unpack_all_archives_in_folder(new_extracted_folder)

                except Exception as e:
                    logger.error(f"Error extracting archive {file_path}: {e}")


def is_archive(file_path):
    """
    Проверяет, является ли файл архивом по его расширению.
    """
    archive_extensions = ['.7z', '.zip', '.tar.gz', '.tgz', '.bz2', '.tar', '.tbz']
    return any(file_path.lower().endswith(ext) for ext in archive_extensions)


if __name__ == "__main__":
    root_folder = r"D:\logs\add\Daily_Checks_20241003104622\InfoCollect\d18k-pair651m"  # Здесь укажите путь к папке с архивами
    unpack_all_archives_in_folder(root_folder)

