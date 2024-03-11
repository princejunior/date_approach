from django.db import models

class ConversationLog(models.Model):
    """
    A model representing a log entry for a conversation.
    Stores information about the speaker, their message, and the timestamp of the log entry.

    Fields:
    - speaker: The name or identifier of the speaker in the conversation.
    - message: The content of the message spoken by the speaker.
    - timestamp: The date and time when the message was recorded, automatically set when the model instance is created.
    """

    # The speaker's name or identifier, limited to 100 characters.
    # You might adjust the max_length based on the expected length of speaker names in your application.
    speaker = models.CharField(max_length=100)

    # The message content. TextField is used to accommodate messages of varying lengths,
    # including potentially long messages.
    message = models.TextField()

    # The timestamp of when the message was added to the log.
    # auto_now_add=True ensures the timestamp is automatically set to the current date and time
    # when a new model instance is created and saved to the database.
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the ConversationLog model.
        Returns a concise and informative description of a ConversationLog instance,
        useful for debugging and displaying in the Django admin site.
        """
        return f"Conversation by {self.speaker} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        """
        Meta options for the ConversationLog model.
        You can add meta options here to customize the behavior of your model,
        such as ordering options or verbose name definitions.
        """
        # Orders ConversationLog instances by timestamp, with the most recent entries first.
        # This is useful for displaying conversation logs in chronological order.
        ordering = ['-timestamp']
