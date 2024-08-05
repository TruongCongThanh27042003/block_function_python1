def sigma0(x):
    return ((x >> 7) | (x << (32-7))) ^ ((x >> 18) | (x << (32-18))) ^ (x >> 3)

def sigma1(x):
    return ((x >> 17) | (x << (32-17))) ^ ((x >> 19) | (x << (32-19))) ^ (x >> 10)

class BlockFunction:
    def __init__(self):
        self.mreg = [0] * 16
        self.iteration = 0

    def process(self, data_in, flag_0_15):
        if not flag_0_15 and self.iteration < 16:
            self.mreg = [data_in] + self.mreg[:-1]
            self.iteration += 1
        elif flag_0_15 and self.iteration < 64:
            new_word = (sigma1(self.mreg[1]) + self.mreg[6] + sigma0(self.mreg[14]) + self.mreg[15]) & 0xFFFFFFFF
            self.mreg = [new_word] + self.mreg[:-1]
            self.iteration += 1
        
        return self.mreg[0], self.iteration

def simulate_testbench():
    bf = BlockFunction()
    print("Simulating testbench...")
    
    # First 16 iterations (flag_0_15 = 0)
    for i in range(16):
        mreg_15, iteration = bf.process(i, False)
        print(f"Time: {(i+1)*10} | Data In: {i} | Mreg_15: {mreg_15} | Iteration Out: {iteration}")
    
    # Next 48 iterations (flag_0_15 = 1)
    for i in range(16, 64):
        mreg_15, iteration = bf.process(0, True)
        print(f"Time: {(i+1)*10} | Mreg_15: {mreg_15} | Iteration Out: {iteration}")

if __name__ == "__main__":
    simulate_testbench()