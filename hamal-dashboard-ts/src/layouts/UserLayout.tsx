import { MenuDataItem, getMenuData, getPageTitle, DefaultFooter } from '@ant-design/pro-layout';
import { Helmet, HelmetProvider } from 'react-helmet-async';
import { Link, useIntl, ConnectProps, connect } from 'umi';
import React from 'react';
import SelectLang from '@/components/SelectLang';
import { ConnectState } from '@/models/connect';
import logo from '../assets/logo.svg';
import styles from './UserLayout.less';
import { GithubOutlined } from '@ant-design/icons';

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
        <title>{title}</title>
        <meta name="description" content={title} />
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
          {children}
        </div>
        
        {/* UserLayout Footer */}
        <DefaultFooter 
          copyright="2020 Hamal云资源搬运工技术部出品"
          links={[
            {
              key: 'Hamal Dashboard',
              title: 'Hamal Dashboard',
              href: 'https://github.com/JackDan9/hamal/hamal-dashboard-ts',
              blankTarget: true,
            },
            {
              key: 'github',
              title: <GithubOutlined />,
              href: 'https://github.com/JackDan9/hamal',
              blankTarget: true, 
            },
            {
              key: 'Hamal',
              title: 'Hamal',
              href: 'https://github.com/JackDan9/hamal',
              blankTarget: true,
            },
          ]}
          className={styles.footer}
        />
      </div>
    </HelmetProvider>
  );
};

export default connect(({ settings }: ConnectState) => ({ ...settings }))(UserLayout);
