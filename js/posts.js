const POSTS = [
  {
    id: "server-rack",
    title: "Server Rack",
    category: "projects",
    date: "2025-01-26",
    excerpt: "My custom 10 inch server rack made from ikea parts",
    featured: true
  },
  {
    id: "lunar-eclipse-2025",
    title: "2025 Lunar Eclipse",
    category: "astronomy",
    date: "2025-03-14",
    excerpt: "Pictures I took of the lunar eclipse in March 2025",
    featured: true
  },
  {
    id: "orion-nebula-march-2025",
    title: "Orion Nebula - March 2025",
    category: "astronomy",
    date: "2025-03-23",
    excerpt: "Pictures I took of the Orion Nebula on March 23, 2025",
    featured: true
  },
  {
    id: "custom-pc",
    title: "Custom PC Build",
    category: "projects",
    date: "2022-05-26",
    excerpt: "My custom PC build with an Intel i5-12600K and an RTX 3060",
    featured: true
  },
];

const CATEGORIES = {
  projects:  { label: "projects",  icon: ">_", description: "Things I've built, broken, and repaired" },
  racing:    { label: "racing",    icon: ">>", description: "Karting and sim racing" },
  astronomy: { label: "astronomy", icon: ".*", description: "Pictures I've taken of the night sky" }
};
