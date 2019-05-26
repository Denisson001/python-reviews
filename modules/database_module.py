import sqlite3 as sql
import modules.datetime_helper as helper


DATABASE_FILE_PATH = None


def init_database_module(database_file_path):
    global DATABASE_FILE_PATH
    DATABASE_FILE_PATH = database_file_path
    with sql.connect(DATABASE_FILE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications(
                chat_id INTEGER,
                city VARCHAR(255),
                update_dttm TEXT
            )
        ''')
        connection.commit()


def add_notification(chat_id, city, event_tm):
    if helper.compare_timestamps(event_tm, helper.get_current_time()):
        update_dttm = helper.get_current_date() + ' ' + event_tm
    else:
        update_dttm = helper.get_tomorrow_date() + ' ' + event_tm

    with sql.connect(DATABASE_FILE_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute('''
            SELECT EXISTS(
                SELECT chat_id, city, time(update_dttm) as update_tm
                FROM notifications
                WHERE chat_id = :chat_id
                AND city = :city
                AND time(update_dttm) = :event_tm
            )
        ''', {"chat_id": chat_id, "city": city, "event_tm": event_tm})

        exists = cursor.fetchone()[0]

        if exists:
            message = 'Notification is already added!'
        else:
            cursor.execute('''
                INSERT INTO notifications VALUES(:chat_id, :city, :update_dttm)
           ''', {"chat_id": chat_id, "city": city, "update_dttm": update_dttm})
            connection.commit()
            message = 'Notification successfully created!'

    return message


def get_user_notifications(chat_id):
    with sql.connect(DATABASE_FILE_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute('''
            SELECT city, update_dttm
            FROM notifications
            WHERE chat_id = :chat_id
            ORDER BY time(update_dttm), city
        ''', {"chat_id": chat_id})

        notifications = cursor.fetchall()

    messages = list()
    for i in range(len(notifications)):
        notification = notifications[i]
        message = str(i + 1) + '. '
        message += 'City: ' + notification[0] + '\n'
        message += 'Next notification time: ' + str(notification[1]) + '\n'
        messages.append(message)

    if not len(messages):
        return 'You have not created any notifications yet.', 0

    return ''.join(messages), len(messages)


def get_unprocessed_notifications():
    with sql.connect(DATABASE_FILE_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute('''
            SELECT *
            FROM notifications
            WHERE update_dttm <= :current_timestamp
        ''', {"current_timestamp": helper.get_current_timestamp()})

        notifications = cursor.fetchall()

        cursor.execute('''
            UPDATE notifications
            SET update_dttm = datetime(update_dttm, '+1 day')
            WHERE update_dttm <= :current_timestamp
        ''', {"current_timestamp": helper.get_current_timestamp()})

        connection.commit()

    return notifications


def remove_notifications(chat_id, notification_numbers):
    with sql.connect(DATABASE_FILE_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute('''
               SELECT city, time(update_dttm) as update_tm
               FROM notifications
               WHERE chat_id = :chat_id
               ORDER BY time(update_dttm), city
           ''', {"chat_id": chat_id})

        notifications = cursor.fetchall()

        for num in notification_numbers:
            if num <= 0 or num > len(notifications):
                return 'Wrong input format. Operation aborted.'

        for num in notification_numbers:
            notification = notifications[num - 1]
            cursor.execute('''
               DELETE
               FROM notifications
               WHERE chat_id = :chat_id
               AND city = :city
               AND time(update_dttm) = :update_dttm
            ''', {"chat_id": chat_id, "city": notification[0], "update_dttm": notification[1]})

        connection.commit()

    return 'Operation completed successfully!'
