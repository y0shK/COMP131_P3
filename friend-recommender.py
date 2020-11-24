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
        print(jaccard_dict)




        # find friends in common - numerator

        # total friends - friend A + B


        #jaccard_index =

        # friend dictionary
        #dict_friends = {}


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

    network.suggest_friend("francis")


    #network = create_network_from_file('simple.network')
    #print(network.to_dot())
    #print(network.suggest_friend('francis'))


if __name__ == '__main__':
    main()
