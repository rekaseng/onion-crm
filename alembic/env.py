from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.config import settings

from src.infrastructure.orm.order_orm_model import Base
from src.infrastructure.orm.machine_contracts_orm_model import Base
from src.infrastructure.orm.machines_orm_model import Base
from src.infrastructure.orm.member_group_coupons_orm_model import Base
from src.infrastructure.orm.user_coupon_usage_orm_model import Base
from src.infrastructure.orm.coupon_orm_model import Base
from src.infrastructure.orm.coupon_definition_orm_model import Base
from src.infrastructure.orm.reward_point_orm_model import Base
from src.infrastructure.orm.reward_rule_orm_model import Base

from src.infrastructure.orm.member_group_users_orm_model import Base
from src.infrastructure.orm.member_groups_orm_model import Base
from src.infrastructure.orm.store_credit_transaction_orm_model import Base
from src.infrastructure.orm.store_credits_orm_model import Base
from src.infrastructure.orm.user_qr_keys_orm_model import Base
from src.infrastructure.orm.user_role_orm_model import Base
from src.infrastructure.orm.refresh_token_orm_model import Base
from src.infrastructure.orm.user_orm_model import Base
from src.infrastructure.orm.role_orm_model import Base
from src.infrastructure.orm.tenant_orm_model import Base
from src.infrastructure.orm.permissions_orm_model import Base
from src.infrastructure.orm.user_coupon_orm_model import Base
from src.infrastructure.orm.sku_orm_model import Base
from src.infrastructure.orm.payment_orm_model import Base
from src.infrastructure.orm.otp_orm_model import Base
from src.infrastructure.orm.payment_method_orm_model import Base
from src.infrastructure.orm.transaction_orm_model import Base
from src.infrastructure.orm.user_message_orm_model import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    url = settings.POSTGRES_SYNC_CONNECTION_STRING
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section, {})
    configuration['sqlalchemy.url'] = settings.POSTGRES_SYNC_CONNECTION_STRING
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
