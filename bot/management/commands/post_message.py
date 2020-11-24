import os
import json
import random
from pprint import pprint
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from slackclient import SlackClient

from .utils import get_questions

class Command(BaseCommand):
    help = 'Posts a message to a slack channel'

    def handle(self, *args, **options):
        questions = get_questions()
        question = random.choice(questions)

        slack_token = "xoxp-486700640898-486900346853-488834356774-61448a1337062cc7906af70aeb40ee90"
        sc = SlackClient(slack_token)

        # Create channel
        channel = "scrum_quizz"
        create_channel_call = sc.api_call(
            "channels.join",
            name=channel
        )
        should_invite_people = (
            create_channel_call["ok"] and not
            create_channel_call["already_in_channel"])

        # Obtain people to invite
        users_call = sc.api_call(
            "users.list"
        )
        if create_channel_call["ok"] and users_call["ok"]:
            for user in users_call['members']:
                if not user["is_bot"]:
                    sc.api_call(
                        "channels.invite",
                        channel=create_channel_call["channel"]["id"],
                        user=user["id"]
                    )
        # Bot
        slack_bot_token = "xoxb-486700640898-488834357606-uC7yN4PqNQsPjDxioNIGUgiK"
        sc = SlackClient(slack_bot_token)
        slack_response = sc.api_call(
            "chat.postMessage",
            channel=channel,
            text="*{} > {}* \n *Q:* {} \n  *A:* {}".format(*question),
            attachments=[
                dict(
                    text="Was this useful?",
                    color="#3AA3E3",
                    actions=[{
                        "name": "usefulness",
                        "text": "Yes",
                        "type": "button",
                        "value": "yes"
                    },
                    {
                        "name": "usefulness",
                        "text": "No",
                        "style": "danger",
                        "type": "button",
                        "value": "no",
                        "confirm": {
                            "title": "Are you sure?",
                            "text": "Our team worked very hard on it!",
                            "ok_text": "I don't care",
                            "dismiss_text": "Fine"
                        }
                    }]
                )
            ]
        )

        if not slack_response["ok"]:
            raise CommandError('Poll "%s" does not exist' )
        else:
            self.stdout.write(self.style.SUCCESS(
                'Successfully posted message to channel "%s"' % channel))


