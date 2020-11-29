#!/usr/bin/env python3


class SocialNetwork:

    def __init__(self):
        '''Constructor; initialize an empty social network
        '''
        self.users = {}

    def list_users(self):
        '''List all users in the network

        Returns:
            [str]: A list of usernames
        '''
        # the user will be the key, while the list of the user's friends is the value
        return list(self.users.keys())

    def add_user(self, user):
        '''Add a user to the network

        This user will have no friends initially.

        Arguments:
            user (str): The username of the new user

        Returns:
            None
        '''
        # the user has no initial friends - this is an empty list of friends for the value
        self.users[user] = []

        #print(self.users[user])
        #print("hi")

    def add_friend(self, user, friend):
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
        #self.users[user] = friend

        # for the empty list of friends for each user, append all of user's friends
        self.users[user].append(friend)
        #users[user] = friend
        #print(user)
        # print(friend)
        #print(self.users[user])




    def get_friends(self, user):
        '''Get the friends of a user

        Arguments:
            user (str): The username of the user whose friends to return

        Returns:
            [str]: The list of usernames of the user's friends

        '''
        # username - key, list of user's friends - value
        # given the key, get the value
        return self.users[user] # values


    def suggest_friend(self, user):
        '''Suggest a friend to the user

        See project specifications for details on this algorithm.

        Arguments:
            user (str): The username of the user to find a friend for

        Returns:
            str: The username of a new candidate friend for the user
        '''
        # find total friends - denominator

        user_friends = []
        #friend_friends = []
        other_person_friends = []

        jaccard_list = []
        jaccard_dict = {}

        common_friends = 0
        total_friends = 0

        print(user)

        recommended_friend = ''

        for friend in self.get_friends(user):
            user_friends.append(friend)

        for person in self.users.keys():
            if person != user:
                other_person_friends = self.get_friends(person)
                #print(other_person_friends)

                # common?
                for other_person in other_person_friends:
                    if other_person in self.get_friends(user):
                        common_friends += 1
                    total_friends += 1

                total_friends += len(self.get_friends(user))

                jaccard_index = common_friends / total_friends
                jaccard_list.append(jaccard_index)
                jaccard_dict[person] = jaccard_index
                #print(jaccard_index)
                #print(jaccard_list)
        #print(jaccard_dict)

        # whichever friend has the highest Jaccard index is the friend who is most similar
        # from our jaccard dict, find the specific person who has the highest jaccard index
            # this is the key with the highest value

        # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
        highest_jaccard_person = max(jaccard_dict, key=jaccard_dict.get)

        # print(highest_jaccard_person)

        """
        Out of the most similar person's friends, find the one who has the most followers.
            - We won't recommend the most similar person - the pool is the similar person's friends
            - The person cannot already be following the suggested person
            - A person also can't be friends with themselves. 
        """

        # automatically excludes the similar person themselves
        similar_person_friend_list = self.get_friends(highest_jaccard_person)
        #print(similar_person_friend_list)

        list_of_suggestions = []

        # for suggestion in similar_person_friend_list:
        #     if suggestion in user_friends:
        #         pass
        #     elif suggestion == user:
        #         pass
        #     else:
        #         list_of_suggestions.append(suggestion)

        for suggestion in similar_person_friend_list:
            if suggestion not in user_friends and suggestion != user: # add stipulations listed above
                list_of_suggestions.append(suggestion)

        #print(list_of_suggestions)

        if not list_of_suggestions: # what if there are no recommendations? e.g. for Cameron - already follows everyone
            return []

        # assume there are recommendations, because the function has not returned []
        suggestion_dict = {} # we want to create a dictionary of all people we could potentially recommend

        # create a dictionary with each suggested person and their follower count
        for person in list_of_suggestions:
            suggestion_dict[person] = len(self.get_friends(person))

        #print(suggestion_dict)

        # if there are multiple people that could be recommended, recommend the one with the most followers
        person_to_recommend = max(suggestion_dict, key=suggestion_dict.get)
        print(person_to_recommend)

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
    network.to_dot()
    alex_friends = network.get_friends("alex")
    print(alex_friends)
    print(network.get_friends("darcy"))
    print(network.get_friends("bailey"))
    print(network.get_friends("cameron"))

    print('---')

    network.suggest_friend("erin")

if __name__ == '__main__':
    main()
