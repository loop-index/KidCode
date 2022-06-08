authorQuery = """{
  searchUsers(query:"flawed"){
    name
    wikidotInfo{
      wikidotId
    }
    vn: statistics (baseUrl: "http://scp-vn.wikidot.com") {
      pageCount
      totalRating
    }
    en: statistics (baseUrl: "http://scp-wiki.wikidot.com"){
      pageCount
      totalRating
    }
    authorInfos{
      authorPage{
        url
        wikidotInfo{
          title
        }
      }
    }
  }
}"""

scpEnQuery = '''
{searchPages(query:"flawed" filter: {anyBaseUrl: "http://scp-wiki.wikidot.com"}){
    url  
    wikidotInfo {
      title
      rating
      createdBy {
        name
      }
      thumbnailUrl
    }
    alternateTitles{
      title
    }
    translations{
      url
      wikidotInfo{
        title
        rating
        createdBy{
          name
        }
      }
      alternateTitles{
        title
      }
    }
  }
}'''

scpVnQuery = '''
{searchPages(query:"flawed" filter: {anyBaseUrl: "http://scp-vn.wikidot.com/"}){
    url  
    wikidotInfo {
      title
      rating
      createdBy {
        name
      }
      thumbnailUrl
    }
    alternateTitles{
      title
    }
    translationOf{
      url
      wikidotInfo{
        title
        rating
        createdBy{
          name
        }
      }
      alternateTitles{
        title
      }
    }
  }
}'''

lcQuery = '''{
  pages (sort: {order: DESC, key: CREATED_AT}, 
    filter: {anyBaseUrl: "http://scp-wiki.wikidot.com/", 
      notCategory: ["fragment", "deleted", "component"], minRating: 0}){
    edges{
      node {
        url
        wikidotInfo {
          title
          createdBy {
            name
          }
          createdAt
          rating
        }
        alternateTitles {
          title
        }
      }
    }
  }
}'''