from datetime import datetime
import requests


class Anilist:
    def __init__(self):
        self.url = "https://graphql.anilist.co"

    def get_animes(self, filters):
        query = '''
query ($id: Int, $page: Int, $year: Int, $season: MediaSeason, $sort: MediaSort) {
  Page(page: $page) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
      perPage
    }
    media(id: $id, type: ANIME, seasonYear: $year, season: $season, sort: [$sort]) {
      id
      description
      coverImage {
        large
        medium
      }
      bannerImage
      title {
        romaji
      }
      genres
    }
  }
}
'''
        payload = {
            "query": query,
            "variables": {
                "year": 2017,
                "season": "FALL",
                "sort": "POPULARITY_DESC",
                "page": 1
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        resp = requests.post(self.url, headers=headers, json=payload)
        return resp.json()

def get_current_year():
    return datetime.now().timetuple().tm_year

def get_current_season():
    # get the current day of the year
    doy = datetime.now().timetuple().tm_yday

    # "day of year" ranges for the northern hemisphere
    spring = range(80, 172)
    summer = range(172, 264)
    fall = range(264, 355)
    # winter = everything else

    if doy in spring:
        season = 'SPRING'
    elif doy in summer:
        season = 'SUMMER'
    elif doy in fall:
        season = 'FALL'
    else:
        season = 'WINTER'

    return season

if __name__ == '__main__':
    anilist = Anilist()
    # print get_current_season()
    # print get_current_year()
    result = anilist.get_animes({})
    animes = result["data"]["Page"]["media"]
    for anime in animes:
        print anime["title"]

