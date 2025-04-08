using System;
using System.Collections.Generic;

namespace SampleApp.Services
{
    public class UserService
    {
        private static List<string> users = new List<string>();

        public void AddUser(string username)
        {
            if (string.IsNullOrEmpty(username))
            {
                throw new ArgumentException("Username cannot be empty");
            }

            if (!users.Contains(username))
            {
                users.Add(username);
                Console.WriteLine("User added: " + username);
            }
            else
            {
                Console.WriteLine("User already exists: " + username);
            }
        }

        public bool RemoveUser(string username)
        {
            if (users.Contains(username))
            {
                users.Remove(username);
                return true;
            }
            return false;
        }

        public void PrintUsers()
        {
            foreach (var user in users)
            {
                Console.WriteLine(user);
            }
        }
    }
}
