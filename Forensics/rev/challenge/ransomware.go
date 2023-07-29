package main

import (
	"crypto/md5"
	"fmt"
	"io/ioutil"
	"path/filepath"
)

func repeatedKeyXor(data []byte, key []byte) []byte {
	encryptedData := make([]byte, len(data))
	for i := 0; i < len(data); i++ {
		encryptedData[i] = data[i] ^ key[i%len(key)]
	}
	return encryptedData
}

func readAndEncryptFiles(dir string) error {
	files, err := ioutil.ReadDir(dir)
	if err != nil {
		return err
	}

	for _, file := range files {
		filePath := filepath.Join(dir, file.Name())
		if !file.IsDir() {
			data, err := ioutil.ReadFile(filePath)
			if err != nil {
				return err
			}

			// Calculate MD5 hash
			hash := md5.Sum(data)
			md5sum := hash[:]

			// Encrypt the data using repeated key XOR with the MD5 hash
			encryptedData := repeatedKeyXor(data, []byte(md5sum))

			// Write the encrypted data back to the file
			newFilePath := filepath.Join(dir, fmt.Sprintf("%s", file.Name()))
			err = ioutil.WriteFile(newFilePath, encryptedData, 0644)
			if err != nil {
				return err
			}

			fmt.Println("File encrypted and saved to:", newFilePath)
		}
	}

	return nil
}

func main() {
	var dir string
	fmt.Print("path: ")
	fmt.Scanln(&dir)

	err := readAndEncryptFiles(dir)
	if err != nil {
		fmt.Println("Error:", err)
	}
}
