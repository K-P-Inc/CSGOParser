import React, { useState } from 'react';
import { Switch } from '~/components/ui/switch';

const WatchList = () => {
    return (
        <div className="home-container">
            <div className="home-posts">
                <table style={{
                    margin: 'auto'  // Используйте 'auto' для центрирования по горизонтали
                }}>
                    <tr>
                        <td>AK-47</td>
                        <td />
                        <td><Switch id='airplane-mode'/></td>
                    </tr>
                    <tr>
                        <td>AWP</td>
                        <td />
                        <td><Switch id='airplane-mode'/></td>
                    </tr>
                    <tr>
                        <td>M4A1-S</td>
                        <td />
                        <td><Switch id='airplane-mode'/></td>
                    </tr>
                    <tr>
                        <td>M4A4</td>
                        <td />
                        <td><Switch id='airplane-mode'/></td>
                    </tr>
                </table>
            </div>
        </div>
    )
}

export default WatchList;