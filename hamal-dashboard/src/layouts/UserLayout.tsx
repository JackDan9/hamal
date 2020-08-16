import { MenuDataItem, getMenuData, getPageTitle, DefaultFooter } from '@ant-design/pro-layout';
import { Helmet, HelmetProvider } from 'react-helmet-async';
import { Link, useIntl, ConnectProps } from 'umi';
import SelectLang from '@/components/SelectLang';
import React from 'react';
import { GithubOutlined } from '@ant-design/icons';
import logo from '../assets/logo.png';
import styles from './UserLayout.less';

export interface UserLayoutProps extends Partial<ConnectProps> {
    breadcrumbNameMap: {
        [path: string]: MenuDataItem;
    };
}

const UserLayout: React.FC<UserLayoutProps> = (props) => {
    const {
        route = {
            routes: [],
        },
    } = props;
    const { routes = [] } = route;
    const {
        children,
        location = {
            pathname: '',
        },
    } = props;
    const { formatMessage } = useIntl();
    const { breadcrumb } = getMenuData(routes);
    const title = getPageTitle({
        pathname: location.pathname,
        formatMessage,
        breadcrumb,
        ...props,
    });
    return (
        <HelmetProvider>
            <Helmet>
                <title>Hamal Dashboard</title>
                <meta name="description" content="Hamal Dashboard" />
            </Helmet>

            <div className={styles.container}>
                <div className={styles.lang}>
                    <SelectLang />
                </div>
                <div className={styles.content}>
                    <div className={styles.top}>
                        <div className={styles.header}>
                            <Link to="/">
                                <img alt="logo" className={styles.logo} src={logo} />
                                <span className={styles.title}>Hamal</span>
                            </Link>
                        </div>
                        <div className={styles.desc}>Hamal 我们是云资源的搬运工</div>
                    </div>
                    {/* {children} */}
                </div>

                <DefaultFooter 
                    copyright="2020 Hamal云资源搬运工技术部出品"
                    links={[
                        {
                            key: 'Hamal Dashboard',
                            title: 'Hamal Dashboard',
                            href: '',
                            blankTarget: true
                        },
                        {
                            key: 'Hamal Github',
                            title: <GithubOutlined />,
                            href: '',
                            blankTarget: true,
                        },
                        {
                            key: 'Hamal',
                            title: 'Hamal',
                            href: '',
                            blankTarget: true,
                        },
                    ]}
                    className={styles.footer}
                />
            </div>
        </HelmetProvider>
    );
};

export default UserLayout;
// export default connect(({ settings }: ConnectState) => ({ ...settings }))(UserLayout);
