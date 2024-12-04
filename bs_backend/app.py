import click
from flask_migrate import Migrate

from myapp import create_app
from myapp.plugin import db
from myapp.models import User


app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
def dropall(drop):
    db.drop_all()
    click.echo('Drop tables.')


@app.cli.command()
def init():
    """Add default user."""
    # 在 users 表中添加一条数据
    user = User(
        name='test01',
        password='test0101_',
        email='test01@gmail.com',
        sex=1,
        address='zhejiang hangzhou',
        phone='12345678911'
    )
    db.session.add(user)
    try:
        db.session.commit()
        click.echo('Added default user.')
    except Exception as e:
        db.session.rollback()
        click.echo('Error adding default user: ' + str(e))

