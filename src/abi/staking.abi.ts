export const abiJSON = {
  name: "Staking",
  methods: [
    {
      name: "deploy",
      desc: "Deploy a new staking pool",
      args: [
        {
          type: "account",
        },
        {
          type: "asset",
        },
        {
          type: "uint64",
        },
        {
          type: "uint64",
        },
      ],
      returns: {
        type: "void",
      },
    },
    {
      name: "init",
      desc: "Initialise a newly deployed pool. Also used to optin new staked assets",
      args: [
        {
          type: "pay",
        },
        {
          type: "asset",
        },
      ],
      returns: {
        type: "void",
      },
    },
    {
      name: "config",
      desc: "Configure the pool. Pause/Unpause the contract, or change the Admin",
      args: [
        {
          type: "axfer",
        },
        {
          type: "asset",
        },
      ],
      returns: {
        type: "void",
      },
    },
    {
      name: "update",
      desc: "Update the smart contracts approval and clearstate programs",
      args: [],
      returns: {
        type: "void",
      },
    },
    {
      name: "reward",
      desc: "Add rewards to the pool and set the fixed rate of reward",
      args: [
        {
          type: "axfer",
        },
        {
          type: "uint64",
        },
        {
          type: "asset",
        },
      ],
      returns: {
        type: "void",
      },
    },
    {
      name: "deposit",
      desc: "Add staking assets into the pool",
      args: [
        {
          type: "axfer",
        },
        {
          type: "asset",
        },
      ],
      returns: {
        type: "void",
      },
    },
    {
      name: "withdraw",
      desc: "Remove staking or reward assets from the pool",
      args: [
        {
          type: "asset",
        },
        {
          type: "uint64",
        },
        {
          type: "account",
        },
        {
          type: "uint64",
        },
      ],
      returns: {
        type: "void",
      },
    },
  ],
};
