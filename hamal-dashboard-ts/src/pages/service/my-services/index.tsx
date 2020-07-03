import React, { useState, useEffect } from 'react';
import { Card, Steps, Table, Tag, Space, Radio, Divider, Button } from 'antd';
import { SyncOutlined, PlusCircleOutlined, PlayCircleOutlined, PoweroffOutlined, UserOutlined, MinusCircleOutlined, MoreOutlined } from '@ant-design/icons';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import { connect, FormattedMessage, formatMessage } from 'umi';
import { MyServicesStateType } from './model';
import styles from './index.less';

const RadioGroup = Radio.Group;

interface MyServicesProps {

}

const MyServices: React.FC<MyServicesProps> = ({ }) => {
    const columns = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            render: text => <a>{text}</a>,
        },
        {
            title: 'Age',
            dataIndex: 'age',
            key: 'age',
        },
        {
            title: 'Address',
            dataIndex: 'address',
            key: 'address',
        },
        {
            title: 'Tags',
            key: 'tags',
            dataIndex: 'tags',
            render: tags => (
                <>
                    {tags.map(tag => {
                        let color = tag.length > 5 ? 'geekblue' : 'green';
                        if (tag === 'loser') {
                            color = 'volcano';
                        }
                        return (
                            <Tag color={color} key={tag}>
                                {tag.toUpperCase()}
                            </Tag>
                        );
                    })}
                </>
            ),
        },
        {
            title: 'Action',
            key: 'action',
            render: (text, record) => (
                <Space size="middle">
                    <a>Invite {record.name}</a>
                    <a>Delete</a>
                </Space>
            ),
        },
    ];

    const data = [
        {
            key: '1',
            name: 'John Brown',
            age: 32,
            address: 'New York No. 1 Lake Park',
            tags: ['nice', 'developer'],
        },
        {
            key: '2',
            name: 'Jim Green',
            age: 42,
            address: 'London No. 1 Lake Park',
            tags: ['loser'],
        },
        {
            key: '3',
            name: 'Joe Black',
            age: 32,
            address: 'Sidney No. 1 Lake Park',
            tags: ['cool', 'teacher'],
        },
    ];

    const [selectionType, setSelectionType] = useState('checkbox');
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const [loading, setLoading] = useState(false);

    const start = () => {
        setLoading(true);
        setTimeout(() => {
            setSelectedRowKeys([]);
            setLoading(false);
        }, 1000);
    };

    const onSelectChange = (selectedRowKeys: any) => {
        console.log('selectedRowKeys changed: ', selectedRowKeys);
        /**
         * useState()
         */
        setSelectedRowKeys(selectedRowKeys);
    };

    const rowSelection = {
      selectedRowKeys,
      onChange: onSelectChange,
    };
    
    const hasSelected = selectedRowKeys.length > 0;

    return (
        <PageHeaderWrapper content='Active Services'>
            <Card bordered={false}>
                <>
                    <div style={{ marginBottom: 16 }}>
                        <Button type="primary" onClick={start} disabled={!hasSelected} loading={loading}>
                            Reload
                        </Button>

                        <Button 
                            type="primary" 
                            style={{ marginLeft: 8 }} 
                            icon={<PlusCircleOutlined />}
                        >
                            添加虚拟机
                        </Button>

                        <Button 
                            type="primary" 
                            style={{ marginLeft: 8 }} 
                            icon={<PlayCircleOutlined />}
                            disabled={!hasSelected}
                        >
                            打开
                        </Button>

                        <Button 
                            type="primary" 
                            style={{ marginLeft: 8 }} 
                            icon={<PoweroffOutlined />}
                            disabled={!hasSelected}
                        >
                            关闭
                        </Button>

                        <Button 
                            type="primary" 
                            style={{ marginLeft: 8 }}
                            icon={<UserOutlined />}
                            disabled={!hasSelected}
                        >
                            虚拟机控制台
                        </Button>

                        <Button 
                            type="primary" 
                            style={{ marginLeft: 8 }}
                            icon={<MinusCircleOutlined />}
                            disabled={!hasSelected}
                        >
                            删除虚拟机
                        </Button>

                        <Button
                            type="primary"
                            style={{ marginLeft: 8 }}
                            icon={<MoreOutlined />}
                        >
                            更多
                        </Button>
                    </div>

                    <Divider />

                    <Table
                        rowSelection={{
                            type: selectionType,
                            ...rowSelection,
                        }}
                        columns={columns}
                        dataSource={data}
                    />
                </>
            </Card>
        </PageHeaderWrapper>
    );
};

export default connect(({ serviceAndmyServices }: { serviceAndmyServices: MyServicesStateType }) => ({
    current: serviceAndmyServices
}))(MyServices);
