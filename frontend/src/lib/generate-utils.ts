export function generateRandomId(length: number) {
    let id = ""
    const vocab = "abcdefghijklmnopqrstuvwxyz1234567890"

    for (let i=0; i<length; i++) {
        id += vocab[Math.floor(Math.random() * (vocab.length - 1))]
    }
    return id
}

console.log(generateRandomId(10))