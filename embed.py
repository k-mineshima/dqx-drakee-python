from discord import Embed, Colour, TextChannel
from typing import List, Tuple, Dict


def on_error_message(title: str = None, description: str = None, error_message: str = None):
    title = title if title is not None else 'エラーが発生しました'
    description = description if description is not None else '技術的なエラーが発生しました\n何度も発生する場合や、時間がたっても改善が見られない場合は管理者に問い合わせてください'
    embed = Embed(
        title=title,
        description=description,
        color=Colour.red()
    )
    if error_message is not None:
        embed.add_field(name='error:', value=error_message, inline=False)

    return embed


def on_management_notice(event: str, description: str):
    title = 'called from {event}'.format(event=event)
    description = description
    embed = Embed(
        title=title,
        description=description
    )
    return embed


def on_management_error(stacktrace: str, event_name: str):
    embed = Embed(
        title='エラーが発生しました',
        description=stacktrace,
        color=Colour.red()
    )
    embed.add_field(name='イベント名', value=event_name, inline=False)
    return embed


def update_prefix_success(before_prefix: str, after_prefix: str):
    embed = Embed(
        title='プレフィックスを変更しました',
        description='コマンドプレフィックスが {before} から {after} に変更されました'.format(before=before_prefix, after=after_prefix),
        color=Colour.blue()
    )
    return embed


def prefix_missing_required_argument(prefix: str):
    embed = Embed(
        title='引数の個数が正しくありません',
        description='prefix のあとには、1つの文字列だけを入力してください',
        color=Colour.red()
    )
    embed.add_field(name='例', value='{prefix}prefix ?'.format(prefix=prefix), inline=False)
    return embed


def item_not_found(item_id: str):
    title = '__**アイテムが見つかりませんでした**__'
    description = '指定された ID ({item_id}) を持つアイテムが見つかりません。'.format(
        item_id=item_id
    )
    embed = Embed(
        title=title,
        description=description,
        color=Colour.red()
    )
    return embed


def item_already_registered(item_id: str, item_name: str):
    title = '__**すでに登録されているアイテムがあります**__'
    description = '指定された ID の中にすでに登録済みのアイテムがありました。'
    embed = Embed(
        title=title,
        description=description,
        color=Colour.red()
    )
    embed.add_field(
        name=item_name,
        value=item_id,
        inline=False
    )
    return embed


def item_registered(item_list: List[Dict[str, str]]):
    title = '__**アイテムを登録しました**__'
    description = '登録したアイテムは定期的にバザー相場が通知され、バザーコマンドにて相場の確認ができるようになります。'
    embed = Embed(
        title=title,
        description=description,
        color=Colour.blue()
    )
    for item_dict in item_list:
        embed.add_field(
            name=item_dict['item_name'],
            value=item_dict['item_id'] if not item_dict['already_registered'] else 'すでに登録されています',
            inline=False
        )

    return embed


def bazaar_market_price(item_list: List[Tuple[str, int]], is_task: bool = False):
    title = '__**現在のバザー相場**__'
    description = 'ただいまのバザー相場情報をお届けします。' if is_task else ''
    embed = Embed(
        title=title,
        description=description,
        color=Colour.blue()
    )
    for item_name, market_price in item_list:
        embed.add_field(
            name=item_name,
            value='最安値 {gold} G'.format(gold=market_price) if market_price is not None else '取得できませんでした',
        )
    return embed


def delete_item_nothing():
    title = '__**指定されたアイテムは登録されていません**__'
    description = 'アイテム名が間違っているか、アイテムIDが不正な値です。'
    embed = Embed(
        title=title,
        description=description,
        color=Colour.red()
    )
    return embed


def delete_items(deleted_items: List[str]):
    title = '__**アイテムを削除しました**__'
    description = '指定されたアイテムを削除しました。\n今後コマンド及び自動通知で本アイテムの相場は通知されません。'
    embed = Embed(
        title=title,
        description=description,
        color=Colour.blue()
    )
    item_names = '\n'.join(deleted_items)
    embed.add_field(name='__**削除されたアイテム**__', value=item_names, inline=False)
    return embed


def item_registered_list(item_list: List[str]):
    title = '__**登録されているアイテム一覧**__'
    description = '登録されているアイテムは、コマンド及び自動通知でバザー相場を確認することができます。'
    embed = Embed(
        title=title,
        description=description,
        color=Colour.blue()
    )
    item_names = '\n'.join(item_list)
    embed.add_field(name='__**登録されているアイテム**__', value=item_names, inline=False)
    return embed


def item_nothing_registered():
    title = 'アイテムが登録されていません'
    description = 'まずはアイテムを **!bazaar add** コマンドを使って登録してください。'
    embed = Embed(
        title=title,
        description=description,
        color=Colour.blue()
    )
    return embed


def wait_for_get_market_prices():
    title = 'バザーの相場情報を取得しています'
    description = 'この処理には時間がかかります。\n少々お待ちください...。'
    embed = Embed(
        title=title,
        description=description,
        color=Colour.green()
    )
    return embed


def on_strong(filename: str):
    title = '本日の聖守護者のつよさ'
    embed = Embed(
        title=title,
        color=Colour.blue()
    )
    embed.set_image(url='attachment://{filename}'.format(filename=filename))
    return embed


def on_strong_updating_notice():
    title = 'このコマンドは現在利用できません'
    description = '聖守護者の強さを更新しています。\nもうしばらくお待ちください。'
    embed = Embed(
        title=title,
        description=description,
        color=Colour.red()
    )
    return embed


def tengoku_opened(period: Dict[str, str], battle_conditions: List[str], item_conditions: List[str], is_task: bool = False):
    title = '**邪神の宮殿 天獄** {opened_text}'.format(opened_text='が開いた!!' if is_task else '')
    embed = Embed(
        title=title,
        description='@everyone' if is_task else '',
        color=Colour.blue()
    )
    embed.add_field(name='**開催期間**', value='{start}\n～\n{end}'.format(start=period['start_date'], end=period['end_date']), inline=False)
    embed.add_field(name='**戦闘中順不同で発生する条件を３つ達成せよ！**', value='\n'.join(battle_conditions), inline=False)
    embed.add_field(name='**戦闘中配られたどうぐ以外使用できない**', value='\n'.join(item_conditions), inline=False)
    embed.set_image(url='attachment://{filename}'.format(filename='open.png'))
    embed.set_footer(text='情報の更新はリアルタイムではありません。数分程度の遅れはご容赦ください。')
    return embed


def tengoku_closed(is_task: bool = False):
    title = '**邪神の宮殿 天獄** {closed_text}'.format(closed_text='が閉じた...。' if is_task else '')
    embed = Embed(
        title=title,
        description='@everyone' if is_task else '',
        color=Colour.blue()
    )
    embed.set_image(url='attachment://{filename}'.format(filename='close.png'))
    embed.set_footer(text='情報の更新はリアルタイムではありません。数分程度の遅れはご容赦ください。')
    return embed


def tengoku_update_failed():
    title = '情報の取得に失敗しました'
    description = '天獄の情報の取得に失敗しました。\n数分後にやり直してください。\n改善しない場合は、管理者に問い合わせてください。'

    embed = Embed(
        title=title,
        description=description,
        color=Colour.red()
    )
    return embed


def create_tengoku_subscription(channel: TextChannel):
    title = '__**#{channel_name} に天獄の開閉情報を通知します**__'.format(
        channel_name=channel.name
    )
    description = '邪神の宮殿 天獄 が開いた・閉まった時に {channel_mention} へ通知します。'.format(
        channel_mention=channel.mention
    )
    embed = Embed(
        title=title,
        description=description,
        color=Colour.blue()
    )
    return embed


def update_tengoku_subscription(before: TextChannel, after: TextChannel):
    title = '__**通知の送信先が #{before} から #{after} に変更されました**__'.format(
        before=before.name,
        after=after.name
    )
    description = '邪神の宮殿 **天獄** が開いた・閉じた時に {channel_mention} に通知します。'.format(
        channel_mention=after.mention
    )
    embed = Embed(
        title=title,
        description=description,
        color=Colour.blue()
    )
    return embed


def duplicate_subscription(channel: TextChannel):
    title = 'すでに #{channel_name} に通知するように設定されています'.format(
        channel_name=channel.name
    )
    description = '設定済みのため、処理はキャンセルされました'
    embed = Embed(
        title=title,
        description=description,
        color=Colour.red()
    )
    return embed


def create_bazaar_subscription(channel: TextChannel):
    title = '__**#{channel_name} にバザーの相場情報を通知します**__'.format(
        channel_name=channel.name
    )
    description = '毎日 09 時と 21 時にバザーの相場情報を {channel_mention} に通知します。'.format(
        channel_mention=channel.mention
    )
    embed = Embed(
        title=title,
        description=description,
        color=Colour.blue()
    )
    return embed


def update_bazaar_subscription(before: TextChannel, after: TextChannel):
    title = '__**通知の送信先が #{before} から #{after} に変更されました**__'.format(
        before=before.name,
        after=after.name
    )
    description = '毎日 09 時と 21 時にバザーの相場情報を {channel_mention} に通知します。'.format(
        channel_mention=after.mention
    )
    embed = Embed(
        title=title,
        description=description,
        color=Colour.blue()
    )
    return embed

