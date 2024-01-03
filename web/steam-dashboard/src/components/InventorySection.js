// InventorySection.js
import React from 'react';
import './InventorySection.css';

const InventorySection = () => {
  return (
    <div className="main-container" id="inventory-section">
      {/* Здесь можно использовать map для генерации инвентарных предметов */}
      {inventoryItems.map((item, index) => (
        <div key={index} className="inventory-item">
          <img src={item.image} alt={item.name} />
          <p>{item.name}</p>
        </div>
      ))}
    </div>
  );
}

// Пример данных для инвентарных предметов
const inventoryItems = [
  { name: 'Название предмета 1', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhz2v_Nfz5H_uOxh7-Gw_alDL_UlWJc6dF-mNbM8Ij8nVn6rhFtYmyiJ4SWJAc4NQvS8ge9xb3v1J65usmbnCY17CMr5CvYmkG1hgYMMLJencFQUA/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhoyszJemkV4N27q4eZkvL6DLbUkmJE5Ysn3ezE9N3x2ge2qBFtYj_6cofHd1U4YQuBqFa6wOm80JG-vMjPzCZjpGB8sou7-M-F/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAR17PLfYQJP7c-ikZKSqPv9NLPF2D0Av8Ai2byRod_z2gHkqBc-aj31dYLGdQ82NFjX_wPryOvphcXo6JnXiSw0NEnp7Nc/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpoo6m1FBRp3_bGcjhQ08-5q5eDnuPxPK7FqXlY-NF4juz--InxgUG55UdrZWGgd46TJwBqaQ3T_we8xOy5g5a7uMmfyHZh6HRw7SncmRW-hxBSLrs4hZCzftg/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpovbSsLQJfw-bbeQJR4-OmgZKbm_LLPr7Vn35cppAh3bnHrNzw2QDk-RBsNjyhdYfAegY6MAvY_VK9wr-615K8v5_IzSR9-n51mmmH1WU/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhjxszJemkV09-5lpKKqPrxN7LEmyVQ7MEpiLuSrYmnjQO3-UdsZGHyd4_Bd1RvNQ7T_FDrw-_ng5Pu75iY1zI97bhLsvQz/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 1', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhz2v_Nfz5H_uOxh7-Gw_alDL_UlWJc6dF-mNbM8Ij8nVn6rhFtYmyiJ4SWJAc4NQvS8ge9xb3v1J65usmbnCY17CMr5CvYmkG1hgYMMLJencFQUA/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhoyszJemkV4N27q4eZkvL6DLbUkmJE5Ysn3ezE9N3x2ge2qBFtYj_6cofHd1U4YQuBqFa6wOm80JG-vMjPzCZjpGB8sou7-M-F/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAR17PLfYQJP7c-ikZKSqPv9NLPF2D0Av8Ai2byRod_z2gHkqBc-aj31dYLGdQ82NFjX_wPryOvphcXo6JnXiSw0NEnp7Nc/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpoo6m1FBRp3_bGcjhQ08-5q5eDnuPxPK7FqXlY-NF4juz--InxgUG55UdrZWGgd46TJwBqaQ3T_we8xOy5g5a7uMmfyHZh6HRw7SncmRW-hxBSLrs4hZCzftg/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpovbSsLQJfw-bbeQJR4-OmgZKbm_LLPr7Vn35cppAh3bnHrNzw2QDk-RBsNjyhdYfAegY6MAvY_VK9wr-615K8v5_IzSR9-n51mmmH1WU/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhjxszJemkV09-5lpKKqPrxN7LEmyVQ7MEpiLuSrYmnjQO3-UdsZGHyd4_Bd1RvNQ7T_FDrw-_ng5Pu75iY1zI97bhLsvQz/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 1', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhz2v_Nfz5H_uOxh7-Gw_alDL_UlWJc6dF-mNbM8Ij8nVn6rhFtYmyiJ4SWJAc4NQvS8ge9xb3v1J65usmbnCY17CMr5CvYmkG1hgYMMLJencFQUA/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhoyszJemkV4N27q4eZkvL6DLbUkmJE5Ysn3ezE9N3x2ge2qBFtYj_6cofHd1U4YQuBqFa6wOm80JG-vMjPzCZjpGB8sou7-M-F/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAR17PLfYQJP7c-ikZKSqPv9NLPF2D0Av8Ai2byRod_z2gHkqBc-aj31dYLGdQ82NFjX_wPryOvphcXo6JnXiSw0NEnp7Nc/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpoo6m1FBRp3_bGcjhQ08-5q5eDnuPxPK7FqXlY-NF4juz--InxgUG55UdrZWGgd46TJwBqaQ3T_we8xOy5g5a7uMmfyHZh6HRw7SncmRW-hxBSLrs4hZCzftg/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpovbSsLQJfw-bbeQJR4-OmgZKbm_LLPr7Vn35cppAh3bnHrNzw2QDk-RBsNjyhdYfAegY6MAvY_VK9wr-615K8v5_IzSR9-n51mmmH1WU/96fx96fdpx2x?allow_animated=1' },
  { name: 'Название предмета 2', image: 'https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhjxszJemkV09-5lpKKqPrxN7LEmyVQ7MEpiLuSrYmnjQO3-UdsZGHyd4_Bd1RvNQ7T_FDrw-_ng5Pu75iY1zI97bhLsvQz/96fx96fdpx2x?allow_animated=1' },
  // Добавьте остальные предметы здесь
];

export default InventorySection;
