from DevLLine import *

DevL = DEVL_LINE("udfdd4098b6a9c59da3ef958bcabc8e6d:aWF0OiAxNTU1NzY2MTI4ODE2Cg==..EB6MI9LBxB8TRr5KR3CNKeTcz10=",appName="IOS\t8.14.5\tDeVL\t7.0.0")

while True:
	try:
		for _ in DevL.run():
			if _.type == 13:
				DevL.acceptGroupInvitation(_.param1)
			if _.type == 26:
				if _.message.text:
					text = _.message.text.lower()
					_.message.to = _.message._from if not _.message.toType and _.message._from != DevL.profile.mid else _.message.to
					if text == 'klop':
						a = Flex(
								contents= Bubble(
									body=Box(
										layout= 'vertical',
										contents = [Text(text='Ok Anjir',wrap=True)]
										)
									)
								)
						a = DevL.liffReply(_.message.to,a)
						print(a)
	except Exception as e:
		print(e)