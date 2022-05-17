

class CollectOdk:
    """
    initiate object with project name example: 'aULeT7vkY9KojRGg7BX6eh'
    .get_response(
        today=False  ## may not work
        submitted_after,
        submitted_between,
    )
    """
    def __init__(self,project):
        self.endpoints=f'https://kobo.humanitarianresponse.info/assets/{project}/submissions/'
        self.params=urlencode({'format':"json"})
        self.api=f'8c526c468efd08b10fc31fef40d74d9d1a825400'
        self.headers={"Authorization":f"Token {self.api}"}

    def get_url(self,query=None):
        if query is not None:
            query=json.dumps(query)
            url=f'{self.endpoints}?{self.params}&query={query}'
            return url
        return f'{self.endpoints}?{self.params}'

    def get_response(self,today=False,submitted_after=None,submitted_between=None):
        query=None
        
        if today==True:
            today_str=dt.datetime.today().strftime('%Y-%m-%d')
            gt=f'{today_str}T00:01:00+05:45' ## from 12:01 am
            lt=f"{today_str}T23:59:00+05:45"  ##11:59 pm
            query={"start":{"$gt":gt,"$lt":lt}}
            
        if submitted_after is not None: 
            query={"start": {"$gt": submitted_after}}
            
        if submitted_between is not None:
            query={"start": {"$gt": submitted_between[0],"$lt": submitted_between[1]}}
                
        url=self.get_url(query)
        r=requests.get(url,headers=self.headers)
        return r.json()