from django.db import models
from audiofield.fields import AudioField

# Create your models here.

class AudioFile(models.Model):
    name = models.CharField(max_length=50)
    tags = models.CharField(max_length=200)
    parse = models.CharField(max_length=500)
    upload_at = models.DateTimeField(auto_now_add=True) 
    audio_file = AudioField(upload_to='audio', blank=True,
                        ext_whitelist=(".mp3", ".wav", ".ogg"),
                        help_text=("Allowed type - .mp3, .wav, .ogg"))

    def __str__(self):
        return '[%s] %s' % (self.id, self.name)

    class Meta:
        default_permissions = ('add', 'change', 'delete')
        verbose_name = 'audio file'
        verbose_name_plural = 'audio files'

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            file_url = settings.MEDIA_URL + str(self.audio_file)
            player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % (file_url)
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = ('Audio file player')
