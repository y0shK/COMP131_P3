#!/usr/bin/env python3
from typing import List

class SocialNetwork:

    def __init__(self):
        '''Constructor; initialize an empty social network
        '''
        self.users = {}

    def list_users(self) -> List[str]:
        '''List all users in the network

        Returns:
            [str]: A list of usernames
        '''
        # the user will be the key, while the list of the user's friends is the value
        return list(self.users.keys())

    def add_user(self, user: str) -> None:
        '''Add a user to the network

        This user will have no friends initially.

        Arguments:
            user (str): The username of the new user

        Returns:
            None
        '''
        # the user has no initial friends - this is an empty list of friends for the value
        self.users[user] = []

    def add_friend(self, user: str, friend: str) -> None:
        '''Adds a friend to a user

        Note that "friends" are one-directional - this is the equivalent of
        "following" someone.

        If either the user or the friend is not a user in the network, they
        should be added to the network.

        Arguments:
            user (str): The username of the follower
            friend (str): The username of the user being followed

        Returns:
            None
        '''
        # ensure that the user and friend are both in the network
        if user not in self.users:
            self.add_user(user)
        elif friend not in self.users:
            self.add_user(friend)

        # at this point, the user and friend are both in the network

        # for the empty list of friends for the user, add the friend to the user's friend list
        self.users[user].append(friend)

    def get_friends(self, user: str) -> List[str]:
        '''Get the friends of a user

        Arguments:
            user (str): The username of the user whose friends to return

        Returns:
            [str]: The list of usernames of the user's friends

        '''
        # username - key, list of user's friends - value
        # given the key, get the list of values and return them
        return self.users[user] # values


    def suggest_friend(self, user: str) -> str:
        '''Suggest a friend to the user

        See project specifications for details on this algorithm.

        Arguments:
            user (str): The username of the user to find a friend for

        Returns:
            str: The username of a new candidate friend for the user
        '''

        # store user's friends
        user_friends = []

        # store jaccard information
        jaccard_list = [] # raw numbers
        jaccard_dict = {} # number attached to person

        common_friends = 0
        total_friends = 0

        print(user)

        # get all of the user's friends - the user's friends cannot be suggested
        for friend in self.get_friends(user):
            user_friends.append(friend)

        # iterate through all of the people in the system
        for person in self.users.keys():
            if person != user:
                other_person_friends = self.get_friends(person)

                # are the friends in common?
                for other_person in other_person_friends: # iterate, see if current user friend == current friend friend
                    if other_person in self.get_friends(user):
                        common_friends += 1 # is the other person's friend also the user's? track that for jaccard
                    total_friends += 1 # the total number of friends is always incremented - other person's friends

                total_friends += len(self.get_friends(user)) # add user's friends to total

                jaccard_index = common_friends / total_friends # each person's jaccard index
                jaccard_list.append(jaccard_index)
                jaccard_dict[person] = jaccard_index

        # whichever friend has the highest Jaccard index is the friend who is most similar
        # from our jaccard dict, find the specific person who has the highest jaccard index
            # this is the key with the highest value

        # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
        # how do we get the maximum element?

        # https://stackoverflow.com/questions/6783000/which-maximum-does-python-pick-in-the-case-of-a-tie
        # max() picks the first element in case of tie - we're making one suggestion

        highest_jaccard_person = max(jaccard_dict, key=jaccard_dict.get)

        print("most similar: " + highest_jaccard_person)

        """
        Out of the most similar person's friends, find the one who has the most followers.
            - We won't recommend the most similar person - the pool is the similar person's friends
            - The person cannot already be following the suggested person
            - A person also can't be friends with themselves. 
        """

        # get_friends() automatically excludes the similar person themselves
        similar_person_friend_list = self.get_friends(highest_jaccard_person)

        list_of_suggestions = []

        for suggestion in similar_person_friend_list:
            if suggestion not in user_friends and suggestion != user: # add stipulations listed above
                list_of_suggestions.append(suggestion)

        if not list_of_suggestions: # what if there are no recommendations? e.g. for Cameron - already follows everyone
            """
            If there is no immediate suggestion, then sort the list of jaccard indices
                and find the "next most" similar person.
            After finding that person, return their friend list and continue as usual.
            This ensures that each person will get a recommendation unless they have really friended everyone.
            """

            # list(sorted())
            # https://www.geeksforgeeks.org/python-program-to-find-second-maximum-value-in-dictionary/

            # access key with value
            # https://stackoverflow.com/questions/8023306/get-key-by-value-in-dictionary

            # go through all of the keys in the dictionary and find the jaccard value that is second highest
            # then grab the key associated with that specific value
            for i in range(1, len(jaccard_dict.keys())):
                # start at 1 because we're using -i, i.e. second most, ...
                # starting at 0 would give [-0] = [0] = least element
                nth_similar_value = list(sorted(jaccard_dict.values()))[-i] # second most, third most, ...
                nth_similar_value = list(jaccard_dict.values()).index(nth_similar_value) # index of the new person
                nth_similar_key = list(jaccard_dict.keys())[nth_similar_value] # this is the name of the new person

                # all() list comprehension - if the suggested friends are already user's friends, can't suggest them

                # https://thispointer.com/python-check-if-a-list-contains-all-the-elements-of-another-list/
                all_in_user_friends = all(friend in self.get_friends(user) for friend in self.get_friends(nth_similar_key))

                if not all_in_user_friends: # are the friends distinct, and can they be suggested?
                    break

            # assuming we need to find a second match
            # e.g. Erin, Bailey in intermediate.network
            similar_person_friend_list = self.get_friends(nth_similar_key)
            print("second most similar: " + nth_similar_key)

            for suggestion in similar_person_friend_list:
                if suggestion not in user_friends and suggestion != user:  # add stipulations listed above
                    list_of_suggestions.append(suggestion) # we now have a list of recommendations

        # there are recommendations, either because we found the suggested friend first try or eventually found them
        suggestion_dict = {} # we want to create a dictionary of all people we could potentially recommend

        # create a dictionary with each suggested person and their follower count
        for person in list_of_suggestions:
            suggestion_dict[person] = len(self.get_friends(person))

        # in the very rare case that the user has friended EVERYONE else
        if len(self.get_friends(user)) == len(self.users) - 1: # can't friend themselves
            print("no recommendations - already friended entire network")
            return ''

        # if there are multiple people that could be recommended, recommend the one with the most followers
        person_to_recommend = max(suggestion_dict, key=suggestion_dict.get)
        print("recommendation: " + person_to_recommend)

        return person_to_recommend

    def to_dot(self):
        result = []
        result.append('digraph {')
        result.append('    layout=neato')
        result.append('    overlap=scalexy')
        for user in self.list_users():
            for friend in self.get_friends(user):
                result.append('    "{}" -> "{}"'.format(user, friend))
        result.append('}')
        return '\n'.join(result)


def create_network_from_file(filename):
    '''Create a SocialNetwork from a saved file

    Arguments:
        filename (str): The name of the network file

    Returns:
        SocialNetwork: The SocialNetwork described by the file
    '''
    network = SocialNetwork()
    with open(filename) as fd:
        for line in fd.readlines():
            line = line.strip()
            users = line.split()
            network.add_user(users[0])
            for friend in users[1:]:
                network.add_friend(users[0], friend)
    return network


def main():
    network = create_network_from_file('simple.network')
    dot = network.to_dot()

    print(dot)

    network.suggest_friend("alex")

if __name__ == '__main__':
    main()
