from Player import Player

from Profile import Profile

import itertools as iter

import numpy as np


class Game():

    def __init__(self, players):

        self.players = players

        self.profiles = self.createProfiles()

    def createProfiles(self):

        nb_players = len(self.players)

        total_strategies = []

        strategies_profiles = []

        # create an empty numpy list

        profiles = np.empty(len(self.players[0].gain), dtype=object)

        for player in self.players:

            total_strategies.append(player.strategies)

        # combination of strategies
        strategies_profiles = list(iter.product(*total_strategies))

        # generate profiles
        for i in range(0, len(self.players[0].gain)):

            gain = []

            for j in range(0, len(self.players)):

                gain.append(self.players[j].gain[i])

            profile = Profile(strategies_profiles[i], tuple(gain))

            profiles[i] = profile

        return profiles

    def strictlyDominantStrategies(self, p):

        val_row = len(self.players[p].strategies)

        # reecuper les strategies du joueur avec sa ligne de gains s1 (g1,g2,g3)

        rows = self.getPlayerStrategies(p)

        for i in range(0, len(rows)):

            is_dominant = True

            for j in range(0, len(rows)):

                if not (all(rows[i] > rows[j])) and not np.array_equal(rows[i], rows[j]):

                    is_dominant = False
                    break

            if(is_dominant):
                return self.players[p].strategies[i]

        return "No strategy"

    def weaklyDominantStrategies(self, p):

        val_row = len(self.players[p].strategies)

        weakly_dom = []

        rows = self.getPlayerStrategies(p)

        for i in range(0, len(rows)):

            is_dominant = True
            is_weakly = False

            for j in range(0, len(rows)):

                if not (all(rows[i] >= rows[j])) and not np.array_equal(rows[i], rows[j]):

                    is_dominant = False
                    break
                else:

                    if(any(rows[i] != rows[j]) and not np.array_equal(rows[i], rows[j])):
                        is_weakly = True

            if(is_dominant and is_weakly):
                weakly_dom.append(self.players[p].strategies[i])

        return weakly_dom

    # reecupere les strategies du joueur avec sa ligne de gains s1 (g1,g2,g3)
    def getPlayerStrategies(self, p):

        rows = []

        for strategy in self.players[p].strategies:

            row = []

            for profile in self.profiles:

                if(profile.strategies[p] == strategy):
                    row.append(profile.gains[p])

            rows.append(row)

        return np.asarray(rows)

    # reecuper les strategies du joueur selon des profils donnés
    def getStrategies(self, p, players, profiles):

        rows = []

        for strategy in players[p].strategies:

            row = []

            for profile in profiles:

                if(profile.strategies[p] == strategy):
                    row.append(profile.gains[p])

            rows.append(row)

        return rows

    def nashEquilibrium(self):

        nash = []

        bAnswers = []

        for i in range(0, len(self.players)):

            # ramener les meilleures reponses du joueur i
            bAnswers.append(self.getBestAnswer(i))

        bAnswers = np.asarray(bAnswers)

        rows = bAnswers.shape[0]

        # get the best answers of player1

        row1 = bAnswers[0]

        # if every profile in row1 is in

        for profile in row1:

            is_nash = True

            for i in range(1, rows):

                if profile not in bAnswers[i]:

                    is_nash = False
                    break

            if(is_nash):
                nash.append(profile)

        return nash

    # get the best answers of each player p
    def getBestAnswer(self, p):

        bAnswersP = []

        profiles_strategy = []

        # get the profiles of every strategy of player p

        for strategy in self.players[p].strategies:

            profiles_strategy.append(self.getProfilesStrategy(strategy, p))

        profiles_strategy = np.asarray(profiles_strategy)

        rows, cols = profiles_strategy.shape

        for j in range(0, cols):

            rows_profiles = []

            for i in range(0, rows):

                rows_profiles.append(profiles_strategy[i][j])

            # now i got the right profiles and i'll choose its max depending on the player ofc

            maxi = max(rows_profiles, key=lambda pro: pro.gains[p])

            # en cas d'egalité des gains de plusieurs profils

            for profile in rows_profiles:

                if(maxi.gains[p] == profile.gains[p]):

                    bAnswersP.append(profile)

        return bAnswersP

    # reecupere tous les profils ou y a la strategie i a la position du joueur p
    def getProfilesStrategy(self, str, p):

        profiles = []

        for profile in self.profiles:

            if(str in profile.strategies[p]):

                profiles.append(profile)

        return profiles

    def securityLevel(self, p):

        val_row = len(self.players[p].strategies)

        rows = []

        strategies_security = []

        # reecuper les strategies du joueur avec sa ligne de gains s1 (g1,g2,g3)

        for strategy in self.players[p].strategies:

            row = []

            for profile in self.profiles:

                if(profile.strategies[p] == strategy):
                    row.append(profile.gains[p])

            rows.append(row)

        rows = np.asarray(rows)

        # je reecupere le minimum de sa liste
        for row in rows:

            strategies_security.append(min(row))

        return strategies_security, max(strategies_security)

    def paretoOptimal(self):

        pareto_dominances = []

        pareto_opt = []

        for profile1 in self.profiles:

            optimum = True

            profile1_gains = np.asarray(profile1.gains)

            for profile2 in self.profiles:

                dominant = False

                if(not np.array_equal(np.asarray(profile1), np.asarray(profile2))):

                    # conversion to np array
                    profile2_gains = np.asarray(profile2.gains)

                    # si profil 2 domine profil 1 on l ajoute a la liste et profil 1 n'est pas pareto dominant

                    if(all(profile2_gains >= profile1_gains) and any(profile2_gains > profile1_gains)):
                        optimum = False
                        dominant = True

                    if(dominant):
                        pareto_dominances.append((profile2, profile1))

            if(optimum):
                pareto_opt.append(profile1)

        return pareto_opt, pareto_dominances

    def iteratedEliminationOfDominatedStrategies(self, t):

        dominant_strategies = []

        iterate = [True]

        profiles = np.copy(self.profiles)

        players = np.copy(self.players)

        copy_str = []

        # copier les strategies des joueurs
        for i in range(0, len(self.players)):

            copy_str.append((self.players[i].strategies).copy())

        # if we deleted any strategy of any player we loop again

        while any(iterate):

            iterate = []

            strategies = []

            for i in range(0, len(self.players)):

                strategies.append(
                    self.getStrategies(i, players, profiles))

                val, profiles = self.eliminateDominatedStrategies(
                    profiles, strategies[i], i, players, dominant_strategies, t)

                iterate.append(val)

        for i in range(0, len(self.players)):

            self.players[i].strategies = copy_str[i]

        if(not dominant_strategies):

            return ["No equilibrium"], ["There is no dominated strategy"]

        return profiles, dominant_strategies

    def eliminateDominatedStrategies(self, profiles, strategies, p, players, dominant, t):

        delete_array = []  # this array contains the index of the strategies to delete

        temp_profiles = []  # this array contains the after-deleting profiles array

        # this array contains the after-deleting  strategies array from players
        temp_strategies = []

        if t == 0:

            eliminate, delete_array = self.eliminateStrictlyDominated(
                strategies, players, dominant, p)
        else:

            eliminate, delete_array = self.eliminateWeaklyDominated(
                strategies, players, dominant, p)

        for value in delete_array:

            temp_profiles = []

            for profile in profiles:

                if((players[p].strategies[value] not in profile.strategies) and (profile not in temp_profiles)):

                    temp_profiles.append(profile)

            if(temp_profiles):
                profiles = np.copy(temp_profiles)

        for i in range(0, len(players[p].strategies)):

            is_available = True

            for value in delete_array:

                if(i == value):
                    is_available = False
                    break

            if(is_available):
                temp_strategies.append(players[p].strategies[i])

        if(temp_profiles):
            profiles = np.copy(temp_profiles)

        if(temp_strategies):
            players[p].strategies = np.copy(temp_strategies)

        return eliminate, profiles

    def eliminateStrictlyDominated(self, strategies, players, dominant, p):

        delete_array = []  # this array contains the index of the strategies to delete

        eliminate = False

        strategies = np.asarray(strategies)

        for i in range(0, len(strategies)):

            for j in range(0, len(strategies)):

                if(i != j):

                    if(all(strategies[i] > strategies[j])):

                        eliminate = True

                        # on elimine les profiles ou il y a la strategie
                        delete_array.append(j)

                        dominant.append(
                            players[p].strategies[j] + " is strictly dominated by " + players[p].strategies[i])

        return eliminate, delete_array

    def eliminateWeaklyDominated(self, strategies, players, dominant, p):

        delete_array = []  # this array contains the index of the strategies to delete

        eliminate = False

        strategies = np.asarray(strategies)

        for i in range(0, len(strategies)):

            for j in range(0, len(strategies)):

                if(i != j):

                    if(all(strategies[i] >= strategies[j])):

                        if(any(strategies[i] > strategies[j])):

                            eliminate = True

                            # on elimine les profiles ou il y a la strategie
                            delete_array.append(j)

                            dominant.append(
                                players[p].strategies[j] + " is dominated by " + players[p].strategies[i])

        return eliminate, delete_array
