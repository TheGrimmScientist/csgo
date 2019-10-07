from django.db import models


class UserGame(models.Model):
    """
    Do we want to save which users we saw in which game?
    """
    # game = models.ForeignKey(Game)

    user_name = models.CharField(max_length=50)  # TODO: Confirm length?
    user_id = models.IntegerField()
    rms = models.FloatField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    headshot_p = models.FloatField()


class Game(models.Model):
    esea_game_id = models.IntegerField(primary_key=True)  # Comes from the url

    injestion_date = models.DateTimeField()
    match_start_time = models.DateTimeField(null=True)
    match_end_time = models.DateTimeField(null=True)

    team_a_score = models.IntegerField(null=True)
    team_b_score = models.IntegerField(null=True)

    player_1_a = models.ForeignKey(
        UserGame, related_name='p1a', on_delete=models.CASCADE, null=True)
    player_2_a = models.ForeignKey(
        UserGame, related_name='p2a', on_delete=models.CASCADE, null=True)
    player_3_a = models.ForeignKey(
        UserGame, related_name='p3a', on_delete=models.CASCADE, null=True)
    player_4_a = models.ForeignKey(
        UserGame, related_name='p4a', on_delete=models.CASCADE, null=True)
    player_5_a = models.ForeignKey(
        UserGame, related_name='p5a', on_delete=models.CASCADE, null=True)

    player_1_b = models.ForeignKey(
        UserGame, related_name='p1b', on_delete=models.CASCADE, null=True)
    player_2_b = models.ForeignKey(
        UserGame, related_name='p2b', on_delete=models.CASCADE, null=True)
    player_3_b = models.ForeignKey(
        UserGame, related_name='p3b', on_delete=models.CASCADE, null=True)
    player_4_b = models.ForeignKey(
        UserGame, related_name='p4b', on_delete=models.CASCADE, null=True)
    player_5_b = models.ForeignKey(
        UserGame, related_name='p5b', on_delete=models.CASCADE, null=True)
    INVALID = 'I'
    FORFEIT = 'F'
    BASE = 'B'
    EXTENDED = 'E'
    GAME_TYPE = [
        (INVALID, 'Invalid'),
        (FORFEIT, 'Forfeit'),
        (BASE, 'Base'),
        (EXTENDED, 'Extended'),
    ]
    game_type = models.CharField(
        max_length=1,
        choices=GAME_TYPE
    )

    # on_delete docs: https://stackoverflow.com/a/38389488/1224255
