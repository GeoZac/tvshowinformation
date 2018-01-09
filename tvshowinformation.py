import urllib.request, json

class showInformation(object):
    def __init__(self, show):
        """Initiates all the variables required for the functions below to work.

        Args:
            show: String: TV Show used in the URL to lookup information

        Variables:
            self.seasonepisodedict: Dictionary containing the seasons as key with the amount of episodes in that season
            self.show: Show name stored as a lowercase string
            self.infourl: url of API needed to retrieve the information (more importantly, the ID number)
            self.showid: Retrieves ID of the show through API and a seperate function called 'getid'
            self.episodesurl: The url that gets all the information about the episodes of the show.

        Returns:
            N/A

0        Raises:
            N/A
        """
        self.seasonsepisodedict = {}
        self.show = show.lower()
        self.episodenamelist = []
        self.runtimeofepisodes = {}
        self.cast = []
        self.genres = []
        self.infourl = 'http://api.tvmaze.com/singlesearch/shows?q=' + self.show
        self.showid = showInformation.getId(self)
        self.episodesurl = 'http://api.tvmaze.com/shows/' + str(self.showid) + '/episodes'
        self.casturl = 'http://api.tvmaze.com/shows/' + str(self.showid) + '/cast'
        showInformation.populate(self)

    def getJson(link):
        """"Returns JSON from API link

        Args:
            link: string with the link to API where you're extracting the JSON from

        Returns:
            python-decoded JSON of information

        Raises:
            N/A
        """
        with urllib.request.urlopen(link) as url:
            data = (json.loads(url.read().decode()))
        return data

    def getId(self):
        """Retrieves the identification number used to get other information about the show from API

        Args:
            N/A

        Returns:
            N/A

        Raises:
            Exception: If TV Show is not found in API
            Exception: If ID was not found in JSON file
        """
        try:
            data = showInformation.getJson(self.infourl)
        except:
            raise Exception("Couldn't find TV Show!")
        if "id" in data:
            return data["id"]
        else:
            raise Exception('Could not retrieve ID!')
            return False

    def populateCast(self):
        """Populates a list of cast of tv show, and returns it
        
        Args:
            N/A

        Returns:
            Cast members in a list

        Raises:
            N/A
        """
        data = showInformation.getJson(self.casturl)
        cast = []
        for index in data:
            new = index["person"]
            cast.append(new["name"])
        return cast
                    

    def populateGenre(self):
        """Populates a list with genres of TV show, and returns the list

        Args:
            N/A

        Returns:
            Genre(s) in a list

        Raises:
            N/A
        """

        data = showInformation.getJson(self.infourl)
        if "genres" in data:
            return data["genres"]
        else:
            return False

    def populate(self):
        """Populates the seasonsepisodedict with information about the seasons and episodes,
        populates episodenamelist with episode names.

        Args:
            N/A

        Returns:
            N/A

        Raises:
            N/A
        """
        seasons = [0]
        season = 0
        episodes = [0]
        namelist = [[0]]
        runtimelist = [[0]]
        data = showInformation.getJson(self.episodesurl)
        for dicts in data:
            for keys in dicts:
                if keys == "season" and dicts[keys] not in seasons: 
                    seasons.append(dicts[keys])
                    season = dicts[keys]
                    episodes.append(0)
                    namelist.append([0])
                    runtimelist.append([0])
                if keys == "number":
                    episodes[season] += 1
            namelist[season].append(dicts["name"])
            runtimelist[season].append(dicts["runtime"])
            
        for i in range(1, len(seasons)):
            self.seasonsepisodedict[seasons[i]] = episodes[i]

        for i in range(len(namelist)):
            for j in range(len(namelist[i])):
                self.runtimeofepisodes[namelist[i][j]] = runtimelist[i][j]

                           
        self.cast = showInformation.populateCast(self)
        self.genres = showInformation.populateGenre(self)
        self.episodenamelist = namelist
        
    def getSeasons(self):
        """Retrieves the amount of seasons the show has

        Args:
            N/A

        Returns:
            Amount of Seasons in TV Show as an Integer

        Raises:
            N/A
        """
        return(max(self.seasonsepisodedict))

    def getEpisodesTotal(self):
        """Retrieves amount of total episodes the show has

        Args:
            N/A

        Returns:
            Amount of total episodes in the show as Integer

        Raises:
            N/A
        """
        totalepisodes = 0
        for seasons in self.seasonsepisodedict:
            totalepisodes += self.seasonsepisodedict[seasons]
        return totalepisodes

    def getEpisodesInSeason(self, seasonnum):
        """Retrieves amount of episodes in specified season

        Args:
            seasonnum: Season Number that you want to retrieve amount of episodes for

        Returns:
            Amount of episodes in specified season (seasonnum) as an integer.

        Raises:
            N/A
        """
        return self.seasonsepisodedict[seasonnum]

    def getEpisodeName(self, seasonnum, episodenum):
        """Retrieves the episode name from nested list

        Args:
            seasonnum: Season number that you want to retrieve episode name
            episodenum: Episode number that you want to retrieve episode name

        Returns:
            Episode name from specified season and episode

        Raises:
            N/A
        """
        return self.episodenamelist[seasonnum][episodenum]

    def getCast(self):
        """Returns cast list as a string

        Args:
            N/A

        Returns:
            Cast as a string

        Raises:
            N/A
        """
        caststring = ''
        if self.cast == []:
            return 'No Cast List'
        for castmember in self.cast:
            caststring += (castmember)
            if castmember != self.cast[-1]:
                caststring += ', '
        return caststring

    def getGenres(self):
        """Returns genre(s) list as a string

        Args:
            N/A

        Returns:
            Genre(s) as a string

        Raises:
            N/A
        """
        genresstring = ''
        if self.genres == []:
            return 'No Genre Listed'
        for genre in self.genres:
            genresstring += genre
            if genre != self.genres[-1]:
                genresstring += ', '
        return genresstring

    def getTotalRuntime(self):
        """Returns total runtime as an integer

        Args:
            N/A

        Returns:
            Total Runtime of show as an integer

        Raises:
            N/A
        """
        totalRuntime = 0
        for keys in  self.runtimeofepisodes:
            totalRuntime +=  self.runtimeofepisodes[keys]
        return totalRuntime

    def getEpisodeRuntime(self, seasonnum, episodenum):
        """Returns run time of certain episode which is specified by
        season (seasonnum) and the episode (episodenum) in corresponding season

        Args:
            seasonnum: Season Number which corresponds to episode you want to get runtime of
            episodenum: Episode in corresponding season that you want to get runtime of

        Returns:
            Episode runtime as an integer

        Raises:
            N/A
        """
        episodename = showInformation.getEpisodeName(self, seasonnum, episodenum)
        return self.runtimeofepisodes[episodename]
