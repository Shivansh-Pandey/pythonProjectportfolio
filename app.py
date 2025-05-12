
from flask import Flask, render_template, jsonify
import dropbox

app = Flask(__name__)

DROPBOX_ACCESS_TOKEN = "sl.u.AFviVM5Q-dBaqhNizVMKhoBDpGY1_5g8kjWLoq9WO0ZwBeMXPcxeqHQvpRPtnfw9dYHgldDLs-zhH4dmfPxlvYvS5UyQaxoQUmIblPO2VLWG05Bi2nkiUGhISOfss4sDDVZgcL6TZdPUiFLmw8yuBzZLoZeDpCLr1Rc6OXsY-hk45Jhr5IMAUFHLXsfPEH5Ds6acKYUY7PBXGjIDmbjIdJrv4x0l1p26klXu_gpAVWY7qKNclq71HDeVrAmRpxlmt8gOa7PvxUANwk_1Hz-5fXe81isATlPMiKRQ7KIhjhYLdqIEaYHh7iPujFXBgCNdKqFP_FMqm8j2ygYcWcKN2J2LXpGl_rRutWKcOwsSABH0nXx2iZG14I4w3GWQzZ7jfxfpLQd_zhrh1xlyozUN-Qz-II8-jj6EPgULh0j-eyw_r_EChIsju2qzo3U9nzReTQsu0UVGhWExB0njLjxfLUS5cAfD5OVY8MLHRkmkEg9jzyTyfnucQAd5EgHHIYLmYCYRj1fYwTUceOhzJeFYZ-1c3xPl82_I1T3uVNUztkptVD0AmNiGT_eNXu9TvGAqAdS1uzovwmCOOAb48urs-bxr3rj6PavoqIcQkM3X2_wmoruEGr1mvwgAy-tGknGewWHL6aRTe0iXy1dx22GdOMiBRba466M1xWi3emKLTMNOuu22M6L5wvfuHhvR7zB9Cllgry-60w-JHMCmi1dOZhTPzQpimnVSDtZxrOq1whgUYjSBqjG0Buxpaqghrv3_5scnGPHQY1O15QDy5NzdE0k7rSgrx6PGuzWh-H7oBOTqv9AMh1MY-yo5CyHGkJbuPlUO6avpD1MwTkwDl-nEefuHvtMOp0yTTSa5MKPKhMm47jDO8WZzk161tBAzWxyaKBkERHkO6rOSJZx41_HWAVWJJdrZlFqU_yED9lCRwd_1NwaIHngfEXzhOMqvR5Iu6UddyYRJam3a1owzI8-POoKYu7IYxbmYUxt1wF731wWCvc0Z8oSyMERKiXVMHbNRO6hVClACEvrV6JsGhLvhTbFgW3EzQDLLzMd7aDu7qb6Yws4LXgUlClW7lu1dSv5DZesGA66Umkl9Ggbpu8p0wZHf_lBJYGgstPqv_-cqsu85NxANxsLWdxiIvBtiK__6ikAueumJZw_FRhZsAW2zb7HILJtAK05yQVX0PzyW8CATlNdYANhbjfy5_I0Wld-UyU10YfkBks3rM6ijN7438e1cubdWGpyuLw8JmH8HFwIcOK6B2X_Ej8Sh7mDiPIPdzYFgvmXWjp1anj_HDRDe5TMD"
PORTFOLIO_FOLDER_PATH = "/APP"


dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def get_portfolio_items():
    category_files = {}
    all_files = []

    result = dbx.files_list_folder(PORTFOLIO_FOLDER_PATH)
    for entry in result.entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            folder_name = entry.name
            folder_path = entry.path_display
            category_files[folder_name] = []

            sub_result = dbx.files_list_folder(folder_path)
            for sub_entry in sub_result.entries:
                if isinstance(sub_entry, dropbox.files.FileMetadata):
                    link = dbx.files_get_temporary_link(sub_entry.path_display).link
                    file_info = {
                        "name": sub_entry.name,
                        "link": link,
                        "type": get_file_type(sub_entry.name),
                        "category": folder_name
                    }
                    category_files[folder_name].append(file_info)
                    all_files.append(file_info)
    
    category_files["All"] = all_files
    return category_files

def get_file_type(filename):
    ext = filename.lower().split(".")[-1]
    if ext in ["jpg", "jpeg", "png", "gif", "webp"]:
        return "image"
    elif ext in ["mp4", "webm", "mov"]:
        return "video"
    elif ext in ["pdf"]:
        return "pdf"
    else:
        return "other"

@app.route("/")
def index():
    data = get_portfolio_items()
    categories = list(data.keys())
    return render_template("index.html", data=data, categories=categories)

if __name__ == "__main__":
    app.run(debug=True)
